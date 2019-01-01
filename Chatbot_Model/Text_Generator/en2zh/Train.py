import numpy as np
from torch import optim

from Data_gen import TranslationDataset
from Models import EncoderRNN, LuongAttnDecoderRNN
from utils import *


def train(input_variable, lengths, target_variable, mask, max_target_len, encoder, decoder, encoder_optimizer,
          decoder_optimizer):
    # Zero gradients
    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    # Set device options
    input_variable = input_variable.to(device)
    lengths = lengths.to(device)
    target_variable = target_variable.to(device)
    mask = mask.to(device)

    # Initialize variables
    loss = 0
    print_losses = []
    n_totals = 0

    # Forward pass through encoder
    encoder_outputs, encoder_hidden = encoder(input_variable, lengths)
    # print('encoder_outputs.size(): ' + str(encoder_outputs.size()))
    # print('encoder_hidden.size(): ' + str(encoder_hidden.size()))

    # Create initial decoder input (start with SOS tokens for each sentence)
    decoder_input = torch.LongTensor([[SOS_token for _ in range(chunk_size)]])
    decoder_input = decoder_input.to(device)
    # print('decoder_input.size(): ' + str(decoder_input.size()))

    # Set initial decoder hidden state to the encoder's final hidden state
    decoder_hidden = encoder_hidden[:decoder.n_layers]
    # print('decoder_hidden.size(): ' + str(decoder_hidden.size()))

    # Determine if we are using teacher forcing this iteration
    use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False
    # print('use_teacher_forcing: ' + str(use_teacher_forcing))

    # Forward batch of sequences through decoder one time step at a time
    if use_teacher_forcing:
        for t in range(max_target_len):
            decoder_output, decoder_hidden = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            # Teacher forcing: next input is current target
            decoder_input = target_variable[t].view(1, -1)
            # Calculate and accumulate loss
            mask_loss, nTotal = maskNLLLoss(decoder_output, target_variable[t], mask[t])
            loss += mask_loss
            print_losses.append(mask_loss.item() * nTotal)
            n_totals += nTotal
    else:
        for t in range(max_target_len):
            decoder_output, decoder_hidden = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            # No teacher forcing: next input is decoder's own current output
            _, topi = decoder_output.topk(1)
            decoder_input = torch.LongTensor([[topi[i][0] for i in range(chunk_size)]])
            decoder_input = decoder_input.to(device)
            # Calculate and accumulate loss
            mask_loss, nTotal = maskNLLLoss(decoder_output, target_variable[t], mask[t])
            loss += mask_loss
            print_losses.append(mask_loss.item() * nTotal)
            n_totals += nTotal

    # Perform backpropatation
    loss.backward()

    # Clip gradients: gradients are modified in place
    _ = torch.nn.utils.clip_grad_norm_(encoder.parameters(), clip)
    _ = torch.nn.utils.clip_grad_norm_(decoder.parameters(), clip)

    # Adjust model weights
    encoder_optimizer.step()
    decoder_optimizer.step()

    return sum(print_losses) / n_totals


def valid(input_variable, lengths, target_variable, mask, max_target_len, encoder, decoder):
    # Set device options
    input_variable = input_variable.to(device)
    lengths = lengths.to(device)
    target_variable = target_variable.to(device)
    mask = mask.to(device)

    # Initialize variables
    loss = 0
    print_losses = []
    n_totals = 0

    with torch.no_grad():
        # Forward pass through encoder
        encoder_outputs, encoder_hidden = encoder(input_variable, lengths)

        # Create initial decoder input (start with SOS tokens for each sentence)
        decoder_input = torch.LongTensor([[SOS_token for _ in range(chunk_size)]])
        decoder_input = decoder_input.to(device)

        # Set initial decoder hidden state to the encoder's final hidden state
        decoder_hidden = encoder_hidden[:decoder.n_layers]

        for t in range(max_target_len):
            decoder_output, decoder_hidden = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            _, topi = decoder_output.topk(1)
            decoder_input = torch.LongTensor([[topi[i][0] for i in range(chunk_size)]])
            decoder_input = decoder_input.to(device)
            # Calculate and accumulate loss
            mask_loss, nTotal = maskNLLLoss(decoder_output, target_variable[t], mask[t])
            loss += mask_loss
            print_losses.append(mask_loss.item() * nTotal)
            n_totals += nTotal

    return sum(print_losses) / n_totals


def main():
    input_lang = Lang('data/WORDMAP_zh.json')
    output_lang = Lang('data/WORDMAP_en.json')
    print("input_lang.n_words: " + str(input_lang.n_words))
    print("output_lang.n_words: " + str(output_lang.n_words))

    train_data = TranslationDataset('train')
    val_data = TranslationDataset('valid')
    print("len(train_data): " + str(len(train_data)))
    print("len(val_data): " + str(len(val_data)))

    # Initialize encoder & decoder models
    encoder = EncoderRNN(input_lang.n_words, hidden_size, encoder_n_layers, dropout)
    decoder = LuongAttnDecoderRNN(attn_model, hidden_size, output_lang.n_words, decoder_n_layers, dropout)

    # Use appropriate device
    encoder = encoder.to(device)
    decoder = decoder.to(device)

    # Initialize optimizers
    print('Building optimizers ...')
    encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate)

    # Initializations
    print('Initializing ...')
    train_batch_time = AverageMeter()  # forward prop. + back prop. time
    train_losses = ExpoAverageMeter()  # loss (per word decoded)
    val_batch_time = AverageMeter()
    val_losses = AverageMeter()

    best_loss = 100000
    epochs_since_improvement = 0

    # Epochs
    for epoch in range(start_epoch, epochs):
        # Decay learning rate if there is no improvement for 8 consecutive epochs, and terminate training after 20
        if epochs_since_improvement == 20:
            break
        if epochs_since_improvement > 0 and epochs_since_improvement % 8 == 0:
            adjust_learning_rate(decoder_optimizer, 0.8)
            adjust_learning_rate(encoder_optimizer, 0.8)

        # One epoch's training
        # Ensure dropout layers are in train mode
        encoder.train()
        decoder.train()

        start = time.time()

        # Batches
        for i_batch in range(len(train_data)):
            input_variable, lengths, target_variable, mask, max_target_len = train_data[i_batch]
            train_loss = train(input_variable, lengths, target_variable, mask, max_target_len, encoder, decoder,
                               encoder_optimizer, decoder_optimizer)

            # Keep track of metrics
            train_losses.update(train_loss)
            train_batch_time.update(time.time() - start)

            start = time.time()

            # Print status
            if i_batch % print_every == 0:
                print('[{0}] Epoch: [{1}][{2}/{3}]\t'
                      'Batch Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                      'Loss {loss.val:.4f} ({loss.avg:.4f})\t'.format(timestamp(), epoch, i_batch,
                                                                      len(train_data),
                                                                      batch_time=train_batch_time,
                                                                      loss=train_losses))

        # One epoch's validation
        start = time.time()

        # Batches
        for i_batch in range(len(val_data)):
            input_variable, lengths, target_variable, mask, max_target_len = val_data[i_batch]
            val_loss = valid(input_variable, lengths, target_variable, mask, max_target_len, encoder, decoder)

            # Keep track of metrics
            val_losses.update(val_loss)
            val_batch_time.update(time.time() - start)

            start = time.time()

            # Print status
            if i_batch % print_every == 0:
                print('Validation: [{0}/{1}]\t'
                      'Batch Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                      'Loss {loss.val:.4f} ({loss.avg:.4f})\t'.format(i_batch, len(val_data),
                                                                      batch_time=val_batch_time,
                                                                      loss=val_losses))

        val_loss = val_losses.avg
        print('\n * LOSS - {loss:.3f}\n'.format(loss=val_loss))

        # Check if there was an improvement
        is_best = val_loss < best_loss
        best_loss = min(best_loss, val_loss)
        if not is_best:
            epochs_since_improvement += 1
            print("\nEpochs since last improvement: %d\n" % (epochs_since_improvement,))
        else:
            epochs_since_improvement = 0

        save_checkpoint(epoch, encoder, decoder, encoder_optimizer, decoder_optimizer, input_lang, output_lang,
                        val_loss, is_best)

        # Initialize search module
        searcher = GreedySearchDecoder(encoder, decoder)
        for input_sentence, target_sentence in pick_n_valid_sentences(input_lang, output_lang, 10):
            decoded_words = evaluate(searcher, input_sentence, input_lang, output_lang)
            print('> {}'.format(input_sentence))
            print('= {}'.format(target_sentence))
            print('< {}'.format(' '.join(decoded_words)))

        # Reshuffle train and valid samples
        np.random.shuffle(train_data.samples)
        np.random.shuffle(val_data.samples)


if __name__ == '__main__':
    main()
