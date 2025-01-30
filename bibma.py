#!/usr/bin/python3
import bibtexparser as bib
import pandas as pd
import argparse

def check_extension(path: str):
    extension = ''
    index = -1
    tail = path[index]
    while tail != '.':
        extension = tail + extension 
        index -= 1
        tail=path[index]
    return extension

def open_file(path):
    ext = check_extension(path)
    if ext == 'xlsx':
        df = pd.read_excel(path)
    elif ext == 'bib':
        with open(path, 'r+') as file:
            df = bib.load(file)
            df = pd.DataFrame(lib.entries)
    elif ext == 'csv':
        df = pd.read_csv(path)
    else:
        raise RunTimeError
    df['doi'] = df['doi'].apply(lambda x: x if x.startswith('https://') else 'https://' + x)
    df['year'] = df['year'].apply(lambda x: int(x))
    return df


def parse_args():
    parser = argparse.ArgumentParser('Bibtex files manipulation')
    parser.add_argument('-i', '--input', type=str, default=None, help='Path to input file')
    parser.add_argument('-o', '--output', type=str, default=None, help='Path to output file')
    parser.add_argument('-d', '--delete', type=str, default=None, help='Column to delete')
    parser.add_argument('-j', '--join', type=str, default=None, help='Bibtex file to compare')
    parser.add_argument('--datelim', type=int, default=0, help='Use with -d to delete papers published before a specific year')
    return parser.parse_args()

def bibToXlsx(path: str, out: str='newfile', dcol: str=None, cdel: str= None, datelim: int=None) -> None:
    df = open_file(path)
    start = len(df)
    if dcol and not cdel:
        print(f'Dropping \'{dcol}\' column')
        df = df.drop(dcol,axis=1)

    if dcol and cdel:
        #with open(cdel, 'r') as compare_file: 
        print('Comparing and Deleting')       
        ext = check_extension(cdel)
        if ext == 'xlsx':
            print(f'Loading {cdel}')
            df2 = pd.read_excel(cdel)
        else: 
            print('Strange file extension')
            raise NotImplementedError
        
        common_values = pd.merge(df, df2, left_on=dcol, right_on=dcol, how='inner')
        df = df[~df[dcol].isin(common_values[dcol])]
    
    if datelim:
        df = df[df['year'] >= datelim]

    print(f'Deleted lines {start - len(df)}')
    df.to_excel(out, index=False)
    

if __name__ == "__main__":
    args = parse_args()
    convert = False
    dcol = None
    cdel = None
    datelim = None

    if args.input:
        path = args.input
        convert = True
    if args.output:
        out = args.output
    if args.delete:
        dcol = args.delete
        if args.join:
            cdel = args.join
        if args.datelim:
            datelim=args.datelim

    if convert:
        bibToXlsx(path, out, dcol=dcol, cdel=cdel, datelim=datelim)

