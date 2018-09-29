import torch
torch.manual_seed(123)
from torch.autograd import Variable

import matplotlib.pyplot as plt

from config import GENRES
from config import DATAPATH
from data import Data
from set import Set
from model import genreNet
from tqdm import tqdm


def main():
    # ------------------------------------------------------------------------------------------- #
    ## DATA
    #data    = Data(GENRES, DATAPATH)
    #data.make_raw_data()
    #data.save()
    data    = Data(GENRES, DATAPATH)
    data.load()
    # ------------------------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------- #
    ## SET
    #set_    = Set(data)
    #set_.make_dataset()
    #set_.save()
    set_ = Set(data)
    set_.load()

    x_train, y_train    = set_.get_train_set()
    x_valid, y_valid    = set_.get_valid_set()
    x_test,  y_test     = set_.get_test_set()
    # ------------------------------------------------------------------------------------------- #

    TRAIN_SIZE  = len(x_train)
    VALID_SIZE  = len(x_valid)
    TEST_SIZE   = len(x_test)

    net         = genreNet()
    criterion   = torch.nn.CrossEntropyLoss()
    optimizer   = torch.optim.RMSprop(net.parameters(), lr=1e-4, weight_decay=1e-2)

    EPOCH_NUM       = 10
    BATCH_SIZE      = 32

    for epoch in range(EPOCH_NUM):
        inp_train, out_train = Variable(torch.from_numpy(x_train)).float(), Variable(torch.from_numpy(y_train)).long()
        inp_valid, out_valid = Variable(torch.from_numpy(x_valid)).float(), Variable(torch.from_numpy(y_valid)).long()
        # ------------------------------------------------------------------------------------------------- #
        ## TRAIN PHASE # TRAIN PHASE # TRAIN PHASE # TRAIN PHASE # TRAIN PHASE # TRAIN PHASE # TRAIN PHASE  #
        # ------------------------------------------------------------------------------------------------- #
        train_loss  = 0
        optimizer.zero_grad()  # <-- OPTIMIZER
        for i in tqdm(range(0, TRAIN_SIZE, BATCH_SIZE)):
            x_train_batch, y_train_batch = inp_train[i:i + BATCH_SIZE], out_train[i:i + BATCH_SIZE]

            pred_train_batch    = net(x_train_batch)
            loss_train_batch    = criterion(pred_train_batch, y_train_batch)
            train_loss          += loss_train_batch.item()

            loss_train_batch.backward()
        optimizer.step()  # <-- OPTIMIZER

        epoch_train_loss = (train_loss * BATCH_SIZE) / TRAIN_SIZE
        train_sum = 0
        for i in tqdm(range(0, TRAIN_SIZE, BATCH_SIZE)):
            pred_train          = net(inp_train[i:i + BATCH_SIZE])
            indices_train       = pred_train.max(1)[1]
            train_sum           += (indices_train==out_train[i:i + BATCH_SIZE]).sum().item()
        train_accuracy = train_sum / float(TRAIN_SIZE)

        # ------------------------------------------------------------------------------------------------- #
        ## VALIDATION PHASE ## VALIDATION PHASE ## VALIDATION PHASE ## VALIDATION PHASE ## VALIDATION PHASE #
        # ------------------------------------------------------------------------------------------------- #
        valid_loss  = 0
        for i in tqdm(range(0, VALID_SIZE, BATCH_SIZE)):
            x_valid_batch, y_valid_batch = inp_valid[i:i + BATCH_SIZE], out_valid[i:i + BATCH_SIZE]

            pred_valid_batch    = net(x_valid_batch)
            loss_valid_batch    = criterion(pred_valid_batch, y_valid_batch)

            valid_loss          += loss_valid_batch.item()

        epoch_valid_loss = (valid_loss * BATCH_SIZE) / VALID_SIZE
        valid_sum = 0
        for i in tqdm(range(0, VALID_SIZE, BATCH_SIZE)):
            pred_valid      = net(inp_valid[i:i + BATCH_SIZE])
            indices_valid   = pred_valid.max(1)[1]
            valid_sum       += (indices_valid == out_valid[i:i + BATCH_SIZE]).sum().item()
        valid_accuracy = valid_sum / float(VALID_SIZE)

        print("Epoch: %d\t\tTrain loss : %.2f\t\tValid loss : %.2f\t\tTrain acc : %.2f\t\tValid acc : %.2f" % \
              (epoch + 1, epoch_train_loss, epoch_valid_loss, train_accuracy, valid_accuracy))


    '''
    plt.figure(figsize=(10, 4))
    specshow(power_to_db(data_chunks[0]))
    plt.colorbar(format='%+2.0f dB')
    plt.title(TRACKPATH + ' spectrogram')
    plt.tight_layout()
    plt.show()
    '''


if __name__ == '__main__':
    main()





