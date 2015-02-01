#!/usr/bin/env python

import itertools
import string
import time
import os
import getopt
import sys


def count_passwords_to_be_generated(alphabet, password_length):
    return pow((len(alphabet)), password_length)


def create_password_generator(alphabet=string.ascii_letters, length=3):
    return itertools.product(alphabet, repeat=length)


def print_passwords(password_generator):
    for pwd in password_generator:
        print("%s" % (''.join(pwd)))


def write_file(password_file, password_generator, alphabet, password_length):
    start_time = time.time()
    nb_passwords_to_compute = count_passwords_to_be_generated(alphabet, password_length)
    one_percent_passwords = nb_passwords_to_compute / 100

    print("Generating %d passwords of %d characters with alphabet: %s"
          % (nb_passwords_to_compute, password_length, alphabet))

    # We write all the passwords to the result file
    nb_passwords = 0
    percentage_done = 0
    with open(password_file, 'a+') as f:
        for pwd in password_generator:
            if nb_passwords > 0 and one_percent_passwords > 0 and nb_passwords % one_percent_passwords == 0:
                percentage_done += 1
                print("%d percent (%d passwords) has been calculated in %.2f seconds (file size: %d bytes)"
                      % (percentage_done, nb_passwords, time.time() - start_time, os.path.getsize(password_file)))
            f.write(''.join(pwd) + '\n')
            nb_passwords += 1

    print("%d bytes have been written to file %s in %.2f seconds containing %d passwords.\n"
          % (os.path.getsize(password_file), password_file, time.time() - start_time, nb_passwords))


def print_all_passwords_in_range(inf=1, sup=5, password_alphabet=string.ascii_letters):
    length = inf
    while length < (sup + 1):
        password_generator = create_password_generator(password_alphabet, length)
        print_passwords(password_generator)
        length += 1


def usage():
    print("Usage")


def main():
    try:
        # we take all the system arguments from 1 to the end
        opts, args = getopt.getopt(sys.argv[1:], "hcl:g:a:f:", ["help", "lower=", "greater=", "alphabet=", "file="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    if len(opts) == 0 and len(args) == 0:
        usage()
        sys.exit()

    lower = None
    greater = None
    pwd_alphabet = string.ascii_letters + string.digits + string.punctuation
    pwd_file = 'passwords.lst'
    write_to_file = False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("-c", "--count"):
            if lower is not None and greater is not None and greater >= lower > 0:
                length = lower
                counter = 0
                while length < (greater + 1):
                    counter += count_passwords_to_be_generated(pwd_alphabet, length)
                    length += 1
                print("There are %d passwords to be generated." % counter)
            else:
                print("You must specify lower and greater in order to count passwords.")
            sys.exit()
        elif opt in ("-l", "--lower"):
            lower = int(arg)
        elif opt in ("-g", "--greater"):
            greater = int(arg)
        elif opt in ("-a", "--alphabet"):
            pwd_alphabet = str(arg)
        elif opt in ("-f", "--file"):
            pwd_file = str(arg)
            write_to_file = True
        else:
            assert False, "unhandled option"

    if write_to_file:
        length = lower
        if lower is not None and greater is not None and greater >= lower > 0:
            while length < (greater + 1):
                generator = create_password_generator(pwd_alphabet, length)
                write_file(pwd_file, generator, pwd_alphabet, length)
                length += 1
            print("End.")
        else:
            print("You must specify lower and greater in order to process.")
    else:
        if lower is not None and greater is not None and greater >= lower > 0:
            print_all_passwords_in_range(lower, greater, pwd_alphabet)
        else:
            usage()

if __name__ == '__main__':
    main()