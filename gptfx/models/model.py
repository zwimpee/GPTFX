import torch
import torch.nn as nn


class CNNLayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride=stride, padding=padding)
        self.relu = nn.ReLU()

    def forward(self, inputs):
        x = self.conv(inputs)
        x = self.relu(x)
        return x


class ResidualBlock(nn.Module):
    def __init__(self, channels, kernel_size, dilation):
        super().__init__()
        self.causal_conv1 = CausalConv1d(channels, channels, kernel_size, dilation)
        self.causal_conv2 = CausalConv1d(channels, channels, kernel_size, dilation)
        self.skip_conv = nn.Conv1d(channels, channels, 1)
        self.gate = nn.GatedLinearUnit()

    def forward(self, x):
        residual = x
        x1 = self.causal_conv1(x)
        x2 = self.causal_conv2(x)
        x = self.gate(torch.cat((x1, x2), 1))
        skip = self.skip_conv(x)
        x = x + residual
        return x, skip


class LSTMLayer(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, dropout):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout)

    def forward(self, inputs, hidden):
        output, hidden = self.lstm(inputs, hidden)
        return output, hidden

    def init_hidden(self, batch_size, device):
        return (torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
                torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device))


class TransformerBlock(nn.Module):
    def __init__(self, n_heads, n_units, dropout_prob):
        super().__init__()
        self.multi_head_attn = MultiHeadAttention(n_heads, n_units)
        self.layer_norm1 = nn.LayerNorm(n_units)
        self.dropout1 = nn.Dropout(dropout_prob)

        self.feed_forward = nn.Sequential(
            nn.Linear(n_units, 4 * n_units),
            nn.ReLU(),
            nn.Linear(4 * n_units, n_units)
        )
        self.layer_norm2 = nn.LayerNorm(n_units)
        self.dropout2 = nn.Dropout(dropout_prob)

    def forward(self, x, mask=None):
        attn_output, attn_weights = self.multi_head_attn(x, x, x, mask=mask)
        x = self.layer_norm1(x + self.dropout1(attn_output))
        ff_output = self.feed_forward(x)
        x = self.layer_norm2(x + self.dropout2(ff_output))
        return x, attn_weights


class HybridModel(nn.Module):
    def __init__(
        self, cnn_in_channels, cnn_out_channels, cnn_kernel_size, cnn_stride, cnn_padding,
        resnet_channels, resnet_kernel_size, resnet_dilation,
        lstm_input_size, lstm_hidden_size, lstm_num_layers, lstm_dropout,
        transformer_num_heads, transformer_num_units, transformer_dropout_prob
    ):
        super().__init__()

        self.cnn_layer = CNNLayer(cnn_in_channels, cnn_out_channels, cnn_kernel_size, cnn_stride, cnn_padding)

        self.resnet_layer = ResidualBlock(resnet_channels, resnet_kernel_size, resnet_dilation)

        self.lstm_layer = LSTMLayer(lstm_input_size, lstm_hidden_size, lstm_num_layers, lstm_dropout)

        self.transformer_block = TransformerBlock(
            transformer_num_heads,
            transformer_num_units,
            transformer_dropout_prob
        )

    def forward(self, x):
        x = self.cnn_layer(x)

        # Convert the shape from (batch_size, channels, height, width) to (batch_size, sequence_length, input_size)
        # for LSTM layer. This is a naive conversion and the exact reshaping operation would depend on your specific
        # task.
        x = x.view(x.size(0), -1, x.size(1))

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        hidden = self.lstm_layer.init_hidden(x.size(0), device)
        x, hidden = self.lstm_layer(x, hidden)

        x, _ = self.transformer_block(x)

        return x
