#!/usr/bin/env python3
"""Split a given album file into multiple tracks using ffmpeg."""
import csv
import argparse
import subprocess


class Track:
    """Class representing a track in the album."""

    file_extention = ''

    def __init__(self, artist, title, start_time, end_time=None):
        """Initialize track object."""
        self.artist = artist
        self.title = title
        self.start_time = start_time
        self.end_time = end_time

    def make_cmd_str(self):
        """Produce a partial command string for the track."""
        cmd_str = f' -ss {self.start_time} '
        if self.end_time:
            cmd_str += f'-to {self.end_time} '
        cmd_str += f"-metadata title='{self.title}' "
        if self.artist:
            cmd_str += f" -metadata artist='{self.artist}' "

        cmd_str += self._generate_track_filename(Track.file_extention)
        return cmd_str

    def _generate_track_filename(self, extention):
        """Generate track file name from the title of the track."""
        track_filename = ''
        for char in self.title:
            if char in " -,.;:(){}[]`~'":
                track_filename += '_'
            else:
                track_filename += char

        if extention != '':
            track_filename = f'{track_filename}.{extention}'
        else:
            pass

        return track_filename


def get_tracks(csvfilename, delimiter=','):
    """
    Generate Track objects from csv file.

    Read non-empty and non-commented lines from `csvfilename` and,
    return a list of Track objects.
    """
    tracks = []
    with open(csvfilename, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if len(row) != 0 and row[0][0] != '#':
                start, end, title, artist = row
                track = Track(
                    artist=artist.strip(),
                    title=title.strip(),
                    start_time=start.strip(),
                    end_time=end.strip(),
                )
                tracks.append(track)
            else:
                pass
    return tracks


def get_extention(filename):
    """Extract extention from `filename`."""
    idx = filename.rfind('.')
    if idx != -1:
        extention = filename[idx+1::]
    else:
        pass
    return extention


def start(albumfile, csvfile, delimiter):
    """Run the script."""
    Track.file_extention = get_extention(albumfile)
    logfile = open('logfile.txt', 'w')
    tracks = get_tracks(csvfile, delimiter)
    for index, track in enumerate(tracks):
        print(f'{index+1}/{len(tracks)} Extracting Track: {track.title}')
        try:
            subprocess.run(
                f'ffmpeg -i {albumfile} {track.make_cmd_str()}',
                shell=True,
                stdout=logfile,
                stderr=logfile)

        except Exception:
            print(f'Error occured while extracting "{track.title}"')
            print('Terminating')
            logfile.close()
            exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='split an audio file, into multiple tracks using ffmpeg')

    parser.add_argument('albumfile', type=str, nargs=1,
                        help='album file to be splitted')

    parser.add_argument('csvfile', type=str, nargs=1,
                        help='csv file containing metadata')

    parser.add_argument('--delimiter', type=str, nargs=1, default=',',
                        help='delimiter for the csv file, defaults to comma')

    args = parser.parse_args()
    albumfile = args.albumfile[0]
    csvfile = args.csvfile[0]
    delimiter = args.delimiter[0]

    try:
        proc = subprocess.run(['ffmpeg', '-h'], check=True)
        start(albumfile, csvfile, delimiter)

    except subprocess.CalledProcessError:
        print('ffmpeg exicted with non-zero exit code!')
    except FileNotFoundError:
        print('Error: ffmpeg not found!')
    except Exception:
        print('Error: some error occured!')
