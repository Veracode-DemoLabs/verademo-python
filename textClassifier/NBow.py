import torch.nn as nn
import torch
import torchtext.data
import torchtext; torchtext.disable_torchtext_deprecation_warning()

class NBoW(nn.Module):
    def __init__(self, vocab, embedding_dim, output_dim, pad_index):
        super().__init__()
        self.embedding = nn.Embedding(len(vocab), embedding_dim, padding_idx=pad_index)
        self.fc = nn.Linear(embedding_dim, output_dim)
        self.vocab = vocab

    def forward(self, ids):
        # ids = [batch size, seq len]
        embedded = self.embedding(ids)
        # embedded = [batch size, seq len, embedding dim]
        pooled = embedded.mean(dim=1)
        # pooled = [batch size, embedding dim]
        prediction = self.fc(pooled)
        # prediction = [batch size, output dim]
        return prediction
    def predict_sentiment(self, text):
        tokenizer = torchtext.data.utils.get_tokenizer("basic_english")
        tokens = tokenizer(text)
        ids = self.vocab.lookup_indices(tokens)
        tensor = torch.LongTensor(ids).unsqueeze(dim=0)
        prediction = self(tensor).squeeze(dim=0)
        probability = torch.softmax(prediction, dim=-1)
        predicted_class = prediction.argmax(dim=-1).item()
        predicted_probability = probability[predicted_class].item()
        return predicted_class, predicted_probability



def create_model():
    vocab = torch.load("vocab")
    embedding_dim = 300
    output_dim = 2
    pad_index = vocab["<pad>"]
    # Create Model instance
    model = NBoW(vocab, embedding_dim, output_dim, pad_index)
    model.load_state_dict(torch.load("nbow.pt"))
    return model