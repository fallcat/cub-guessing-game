import os
import csv
import random

num_games = 20
num_pages = 5

text_filename1 = 'classes_w_descriptions_aab_ebird.tsv'
text_filename2 = 'classes_w_descriptions_wiki.tsv'
image_dir = 'images/'
classes_filename = 'classes.txt'
html_directory = 'html/'

img_height = "200"

def write_header(htmlfile):
    htmlfile.write('<!doctype html>\n')
    htmlfile.write('<html lang="en">\n')
    htmlfile.write('<head>\n<link rel="stylesheet" href="style.css">\n<script src="script.js"></script>\n</head>\n')
    htmlfile.write('<body>\n')

def write_ending(htmlfile):
    htmlfile.write('</body>\n')
    htmlfile.write('</html>\n')

def get_descriptions(text_filename):
    with open(text_filename, 'rt') as csvfile:
        descriptions = [line.strip().split('\t') for line in csvfile.readlines()]
        descriptions = [line[1] if len(line) > 1 else '' for line in descriptions]
        return descriptions

def choose_description(descriptions, idx):
    des = descriptions[idx]
    candidates = []
    for d in des:
        if len(d) > 0:
            candidates.append(d)
    return random.choice(candidates)

description1 = get_descriptions(text_filename1)
description2 = get_descriptions(text_filename2)
descriptions = [('[aab/ebird] ' + d1, '[wikipedia] ' + d2) for d1, d2 in zip(description1, description2)]

with open(classes_filename, 'rt') as classes_file:
    classes = [line.strip().split()[1] for line in classes_file.readlines()]

for page in range(num_pages):
    teacher_html = f'teacher{page}.html'
    student_html = f'student{page}.html'
    with open(os.path.join(html_directory, teacher_html), 'wt') as teacher_file:
        with open(os.path.join(html_directory, student_html), 'wt') as student_file:
            write_header(teacher_file)
            write_header(student_file)
            classes_idx = list(range(len(classes)))
            for i in range(num_games):
                pos_idx = random.choice(classes_idx)
                neg_idxs = random.sample(classes_idx[:pos_idx] + classes_idx[pos_idx + 1:], 4)

                # teacher file
                teacher_file.write('<div class="example">\n')
                teacher_file.write('<div class="block">\n')

                teacher_file.write(f'<div><h3>class: {classes[pos_idx]}</h3></div>\n')
                teacher_file.write(f'<div>{choose_description(descriptions, pos_idx)}</div>\n')
                teacher_file.write('</div>\n')

                # student file
                student_file.write('<div class="example">\n')
                student_file.write('<div class="block">\n')

                student_file.write(f'<div><h3>{classes[pos_idx]}</h3></div>\n')

                all_idxs = [pos_idx] + neg_idxs
                random.shuffle(all_idxs)
                for idx in all_idxs:
                    pos = True if idx == pos_idx else False
                    image_dir_ = os.path.join(image_dir, classes[idx])
                    image_filenames = [img_file  for img_file in os.listdir(image_dir_) if os.path.isfile(os.path.join(image_dir_, img_file))]
                    img = random.choice(image_filenames)
                    student_file.write(f'<div class="img"><img onclick="showAnswer(this);" src="../images/{classes[idx]}/{img}" height="{img_height}">\n')
                    if pos:
                        student_file.write(f'<div id="#answer{i}-{idx}" class="inner" style="color:green; display:none;">Correct!</div>\n')
                    else:
                        student_file.write(f'<div id="#answer{i}-{idx}" class="inner" style="color:red; display:none;">Incorrect!</div>\n')
                    student_file.write(f'</div>\n')
                student_file.write('</div>\n')

                teacher_file.write('</div>\n')
                student_file.write('</div>\n')


            write_ending(teacher_file)
            write_ending(student_file)
