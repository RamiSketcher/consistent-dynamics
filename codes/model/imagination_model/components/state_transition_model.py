from torch import nn
import torch

from codes.model.base_model import BaseModel


class Model(BaseModel):
    """ State Transition Model."""
    def __init__(self, config):
        super().__init__(config=config)
        self._hidden_state_size = self.config.model.imagination_model.hidden_state_size
        self._input_size = self.config.model.imagination_model.latent_size + self._hidden_state_size
        # Note that the hidden state size corresponds to the encoding of the observation in the pixel space.
        self._num_layers = 1
        self._batch_first = True
        self.h_0 = None
        self.c_0 = None
        self.reset_state()
        self.lstm = nn.LSTM(input_size = self._input_size,
                            hidden_size = self._hidden_state_size,
                            num_layers= self._num_layers,
                            batch_first=self._batch_first)



    def forward(self, x):
        input = x
        output, (self.h_0, self.c_0) = self.lstm(input, (self.h_0, self.c_0))
        return output

    def reset_state(self):
        self.h_0 = None
        self.c_0 = None

    def set_state(self, h_0):
        self.h_0 = h_0.unsqueeze(0).contiguous()
        self.c_0 = torch.zeros_like(self.h_0)