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

def parse_args():
    parser = argparse.ArgumentParser('Bibtex files manipulation')
    parser.add_argument('-i', type=str, default=None, help='Path to input file')
    parser.add_argument('-o', type=str, default=None, help='Path to output file')
    parser.add_argument('-d', type=str, default=None, help='Column to delete')
    parser.add_argument('-c', type=str, default=None, help='Bibtex file to compare')
    parser.add_argument('--datelim', type=int, default=0, help='Use with -d to delete papers published before a specific year')
    return parser.parse_args()

def bibToXlsx(path: str, out: str, dcol: str=None, cdel: str= None, datelim: int=None) -> None:
    with open(path, 'r+') as file:
        lib = bib.load(file)
        df = pd.DataFrame(lib.entries)
        start = len(df)
        df['doi'] = df['doi'].apply(lambda x: x if x.startswith('https://') else 'https://' + x)
        df['year'] = df['year'].apply(lambda x: int(x))

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
    dcol = None
    cdel = None
    datelim = None
    if args.i:
        path = args.i
    if args.o:
        out = args.o
    if args.d:
        dcol = args.d
        if args.c:
            cdel = args.c
        if args.datelim:
            datelim=args.datelim
        
    bibToXlsx(path, out, dcol=dcol, cdel=cdel, datelim=datelim)

