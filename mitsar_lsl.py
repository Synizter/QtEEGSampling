# """Example program to show how to read a multi-channel time series from LSL."""

# from pylsl import StreamInlet, resolve_stream


# def main():
#     # first resolve an EEG stream on the lab network
#     print("looking for an EEG stream...")
#     streams = resolve_stream('type', 'EEG')

#     # create a new inlet to read from the stream
#     inlet = StreamInlet(streams[0])
#     nbr_sample = 10

#     while True:
#         # get a new sample (you can also omit the timestamp part if you're not
#         # interested in it)
#         sample, timestamp = inlet.pull_sample()
#         print(timestamp, sample)
#         if nbr_sample == 0:
#             break
#         nbr_sample -= 1


# if __name__ == '__main__':
#     main()


"""Example program to demonstrate how to read a multi-channel time-series
from LSL in a chunk-by-chunk manner (which is more efficient)."""

from pylsl import StreamInlet, resolve_stream

data =dict()
d = []
time = []

def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    time_shift_correct = inlet.time_correction()
    nbr_chunk = 10
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        chunk, timestamps = inlet.pull_chunk()
        if nbr_chunk:
            if timestamps:
                for t,d in zip(timestamps, chunk):
                    #check key redundant
                    t = t + time_shift_correct
                    if str(t) not in data.keys():
                        data[str(t)] = d
                    else:
                        print('found reduntdant at ', str(t))
                    # d.append((t, d))

                    # print(t + time_shift_correct, d)
                nbr_chunk -= 1
        else:
            break
    

    print(list(data.keys())[0] ,data[list(data.keys())[0]])
if __name__ == '__main__':
    main()