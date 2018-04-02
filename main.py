import sys
from soundbytes import load_sound, play_sound, write_wav

def main():
    path = sys.argv[1]
    start = float(sys.argv[2])
    dest = sys.argv[3]
    end = start + 10  # Default duration of 10s
    resolution = 1
    while True:
        print_status(start, end, resolution)
        display_usage()
        audio = load_sound(path, start, end)
        play_sound(*audio)
        is_done, start, end, resolution = handle_input(
                start, end, resolution, audio, dest)
        if is_done:
            break


def print_status(start, end, resolution):
    print('Start: %f' % start)
    print('End: %f' % end)
    print('Resolution: %f' % resolution)


def display_usage():
    print("Options")
    print("\t( - Start earlier")
    print("\t) - Start later")
    print("\t[ - End earlier")
    print("\t] - End later")
    print("\t< - Shorter increments")
    print("\t> - Longer increments")
    print("\tp - Replay sound")
    print("\ts - Save sound")

def handle_input(start, end, resolution, audio, dest):
    while True:
        choice = input(': ')
        if choice in '()[]<>ps':
            break
        else:
            print('Enter one of ()[]<>ps')
    if choice == '(':
        start -= resolution
    elif choice == ')':
        start += resolution
    elif choice == '[':
        end -= resolution
    elif choice == ']':
        end += resolution
    elif choice == '<':
        resolution /= 2.0
    elif choice == '>':
        resolution *= 2.0
    elif choice == 'p':
        play_sound(*audio)
    elif choice == 's':
        write_wav(dest, *audio)

    is_done = (choice in 'ps')
    return is_done, start, end, resolution

if __name__ == '__main__':
    main()
