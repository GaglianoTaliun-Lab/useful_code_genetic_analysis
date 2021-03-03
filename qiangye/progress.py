import sys
import time

def print_progress(i, time_elapsed = None):
    """show progress of process, often used in training a neural network model
    params
        i: progress value in [0, 1.], double
        time_elapsed: time elapsed from progress 0.0 to current progress, double
        before: descriptive content displayed before progress i, str
        after: descriptive content displayed after progress i, str
    """
    progress_info = '{:>7.2%}'.format(i) # align right, 7 characters atmost
    if time_elapsed is not None:
        progress_info += '; elapsed:{:>3.0f}m{:0>2.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60)
        if i >= 1:
            time_remaining = 0
            progress_info += ". complete."
        elif 0 < i < 1:
            time_remaining = time_elapsed * (1. - i) / i
            progress_info += '; estimated remaining:{:>3.0f}m{:0>2.0f}s'.format(
                time_remaining // 60, time_remaining % 60)
        else:
            progress_info += '; estimated remaining: --m--s'
    

    # display progress repeately in the same line.
    progress_info = '\rProgress:' + progress_info
    line_length = 63 if time_elapsed else 17
    progress_info = progress_info.ljust(line_length, " ")
    sys.stdout.flush()
    sys.stdout.write(progress_info)


if __name__ == "__main__":
    start = time.time() 
    for i in range(101):
        end = time.time()
        print_progress(i/100, end-start)
        time.sleep(0.04)

