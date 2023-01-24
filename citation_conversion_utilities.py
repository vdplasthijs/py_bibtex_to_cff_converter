## Modules for citation file conversion

import os, sys
import bibtexparser
from datetime import datetime 

class Citation():
    def __init__(self, bibtex_filepath=None):
        self.info_dict = {}
        self.bibtex_provided = False
        self.repo_provided = False

        self.bibtex_filepath = bibtex_filepath
        self.load_bibtex_file(filepath=self.bibtex_filepath)


    def load_bibtex_file(self, filepath):
        with open('example_bib_files/pmlr-v199-plas22a.bib') as bf:
            bib_db = bibtexparser.load(bf)

        assert len(bib_db.entries) == 1, 'more than 1 entries in bib tex file, give ind or something'
        bib_info = bib_db.entries[0]
        assert type(bib_info) == dict 

        for key in ['ENTRYTYPE', 'title', 'booktitle', 'pages', 'year', 'month', 'day',
                    'volume', 'series', 'issue', 'editor', 'publisher', 'url', 'doi', 'abstract']:
            if key in bib_info.keys():
                self.info_dict[key] = bib_info[key]
            else:
                self.info_dict[key] = 'N/A'
        
        ## Author info 
        if 'author' in bib_info.keys():
            author_list = bib_info['author'].split(' and ')
            self.info_dict['n_authors'] = len(author_list)
            author_dict = {}
            for ind, author_name in enumerate(author_list):
                assert ',' in author_name, f'No comma (,) in name {author_name}'
                assert len(author_name.split(',')) == 2, f'More than 1 comma (,) in {author_name}'
                author_dict[ind] = {}
                author_dict[ind]['full_name'] = author_name
                author_dict[ind]['first_name'] = author_name.split(',')[0]
                author_dict[ind]['last_name'] = author_name.split(',')[1]
            self.info_dict['author_dict'] = author_dict
            # print(author_list)
        else:
            self.info_dict['author'] = None
       
        self.bibtex_provided = True 

    def input_repo_info(self, repo_url=None, message=None, repo_doi=None, 
                        authors=None):
        if repo_url is not None:
            assert type(repo_url) == str, type(repo_url)
            self.info_dict['repo_url'] = repo_url
        else:
            self.info_dict['repo_url'] = 'N/A'
        if message is not None:
            assert type(message) == str, type(message)
            self.info_dict['message'] = message 
        else:
            self.info_dict['message'] = 'N/A'
        if repo_doi is not None:
            assert type(repo_doi) == str, type(repo_doi)
            self.info_dict['repo_doi'] = repo_doi
        else:
            self.info_dict['repo_doi'] = 'N/A'

        if authors is not None:  # assume authors of repo are different than authors of bibtex file 
            assert False, 'Different authors specified for repo -- no yet implemented.!'

        self.repo_provided = True 

    def prep_info_for_export(self):
        '''Run some checks and make data in order'''
        assert self.bibtex_provided, 'bibtex file not yet provided'
        assert self.repo_provided, 'repo not yet provided'

        idk = self.info_dict.keys()
        find_date = True
        construct_date = False
        while find_date:
            if 'date-released' in idk:
                find_date = False
            elif 'date' in idk:
                self.info_dict['date-released'] = self.info_dict['date']
                find_date = False 
                
            construct_date = True 
            dt = datetime.now()
            if 'year' in idk:
                year = self.info_dict['year']
            else:  # use current date
                year = dt.year 
                month = dt.month 
                day = dt.day 
                find_date = False 
            if 'month' in idk:
                month = self.info_dict['month']
            else:  # if year known but not month, just to 1 Jan
                month = 1 
                day = 1 
                find_date = False 
            if 'day' in idk:
                day = self.info_dict['day']
                find_date = False 
            else:
                day = 1 

        if construct_date:
            self.info_dict['date-released'] = f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}'

    def add_author_names_to_cff(self, filename, indent_n_spaces=0):
        assert type(indent_n_spaces) == int and indent_n_spaces >= 0
        id = ' ' * indent_n_spaces
        assert 'author_dict' in self.info_dict
        ad = self.info_dict['author_dict']
        assert self.info_dict['n_authors'] == len(ad)
        assert len(ad) > 0 

        with open(filename, 'a') as f:  # add 
            f.write(f'{id}authors:\n')
            for i_author, author_name_dict in ad.items():
                f.write(f'{id}  - name-suffix: "N/A"\n')
                f.write(f'{id}    given-names: "{author_name_dict["first_name"]}"\n')
                f.write(f'{id}    name-particle: "N/A"\n')
                f.write(f'{id}    family-names: "{author_name_dict["last_name"]}"\n')

    def export_to_cff(self, cff_version="1.2.0", filename='tmp.cff'):
        
        assert type(cff_version) == str, type(cff_version)
        if filename[-4:] != '.cff':
            filename = filename + '.cff'

        with open(filename, 'w') as f:  # write, so create new file (or overwrite from scratch)
            f.write(f'date-released: "{self.info_dict["date-released"]}"\n')
            f.write(f'repository-code: "{self.info_dict["repo_url"]}"\n')
            f.write(f'message: "{self.info_dict["message"]}"\n')
            f.write(f'doi: "{self.info_dict["repo_doi"]}"\n')
            f.write(f'title: "{self.info_dict["title"]}"\n')
            f.write(f'cff-version: "{cff_version}"\n')

        self.add_author_names_to_cff(filename=filename, indent_n_spaces=0)

        with open(filename, 'a') as f:
            f.write('preferred-citation:\n')
            if 'publisher' in self.info_dict:
                f.write('  publisher:\n')
                f.write(f'    name: "{self.info_dict["publisher"]}"\n')
            for key in ['issue', 'doi', 'date-released', 'volume', 'journal', 'title']:
                if key in self.info_dict.keys():
                    f.write(f'  {key}: "{self.info_dict[key]}"\n')
            
        self.add_author_names_to_cff(filename=filename, indent_n_spaces=2)

        with open(filename, 'a') as f:
            if 'ENTRYTYPE' in self.info_dict.keys():
                f.write(f'  type: "{self.info_dict["ENTRYTYPE"]}"\n')
            else:
                f.write('  type: "generic"\n')

        print(f'Saved to {filename} in {os.getcwd()}/')