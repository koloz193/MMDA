from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import join
from datetime import datetime
from functools import reduce
import uuid
from bs4 import BeautifulSoup
import urllib2
import os
import magic

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/mmda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

"""
-----------------------------Section for Database-----------------------------
"""

class DAGR(db.Model):
    __tablename__ = 'DAGR'
    GUID = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    path = db.Column(db.String(256))
    date_created = db.Column(db.String(10))
    date_modified = db.Column(db.String(10))
    annotations = db.Column(db.String(256))

    file_type = db.Column(db.String(16))

    owner = db.Column(db.String(64), db.ForeignKey('Author.GUID'), nullable=False)
    author = db.relationship('Author')

    def __repr__(self):
        return '<Name: %r, Annotations: %r>' % (self.name, self.annotations)

    def getName(self):
        return self.name;

    def getGUID(self):
        return self.GUID;

    def getType(self):
        return self.file_type

    def getPath(self):
        parent = ParentChild.query.filter_by(child_guid=self.GUID).first()

        return "" if parent is None else DAGR.query.filter_by(GUID=parent.parent_guid).first().getShortPath() + '|' + DAGR.query.filter_by(GUID=parent.parent_guid).first().getName()

    def getShortPath(self):
        parent = ParentChild.query.filter_by(child_guid=self.GUID).first()

        return "" if parent is None else DAGR.query.filter_by(GUID=parent.parent_guid).first().getName()

    def getCreated(self):
        return self.date_created

    def getModified(self):
        return self.date_modified

    def getAnnotations(self):
        return self.annotations

    def getAuthor(self):
        return Author.query.filter_by(GUID=self.owner).first()

    def getAuthorName(self):
        return Author.query.filter_by(GUID=self.owner).first().getName()

class Author(db.Model):
    __tablename__ = 'Author'
    name = db.Column(db.String(64))
    GUID = db.Column(db.String(64), primary_key=True)

    def __repr__(self):
        return '<Author: %r>' % self.name

    def getName(self):
        return self.name

    def getGUID(self):
        return self.GUID

class ParentChild(db.Model):
    __tablename__ = 'ParentChild'
    parent_guid = db.Column(db.String(64), db.ForeignKey('DAGR.GUID'), primary_key=True)
    child_guid = db.Column(db.String(64), db.ForeignKey('DAGR.GUID'), primary_key=True)

    def __repr__(self):
        return '<Parent: %r, Child: %r>' % (self.parent_guid, self.child_guid)

    def getParentGUID(self):
        return self.parent_guid

    def getChildGUID(self):
        return self.child_guid

def new_dagr(dagr_name, dagr_annotations, parent_dagr, author_name='Zach'):
    guid = str(uuid.uuid4())
    creation = datetime.today().strftime('%Y-%m-%d')
    modified = datetime.today().strftime('%Y-%m-%d')

    if parent_dagr != "new":
        p = DAGR.query.filter_by(name=parent_dagr).first()
        p_guid = p.getGUID()
        parent_path = p.getPath()
        pc = ParentChild(parent_guid=p_guid, child_guid=guid)
        db.session.add(pc)
    else:
        parent_path = ""

    if Author.query.filter_by(name=author_name).first() == None:
        author_guid = str(uuid.uuid4())
        author = Author(name=author_name, GUID=author_guid)
        db.session.add(author)
    else:
        author_guid = Author.query.filter_by(name=author_name).first().getGUID()

    path = parent_path + "|" + dagr_name

    dagr = DAGR(name=dagr_name, annotations=dagr_annotations, GUID=guid, date_created=creation, date_modified=modified, owner=author_guid, file_type="DAGR", path=path)
    db.session.add(dagr)
    db.session.commit()

def add_file_to_dagr(dagr_name, file_name, file_annotations, file_type='HTML', author_name='Zach'):
    guid = str(uuid.uuid4())
    creation = datetime.today().strftime('%Y-%m-%d')
    modified = datetime.today().strftime('%Y-%m-%d')

    if Author.query.filter_by(name=author_name).first() == None:
        author_guid = str(uuid.uuid4())
        author = Author(name=author_name, GUID=author_guid)
        db.session.add(author)
    else:
        author_guid = Author.query.filter_by(name=author_name).first().getGUID()

    dagr = DAGR.query.filter_by(name=dagr_name).first()
    dagr_guid = dagr.getGUID()
    dagr_path = dagr.getPath()

    file_path = dagr_path

    pc = ParentChild(parent_guid=dagr_guid, child_guid=guid)
    db.session.add(pc)

    new_file = DAGR(name=file_name, GUID=guid, path=file_path, date_created=creation, date_modified=modified, owner=author_guid, annotations=file_annotations, file_type=file_type)
    db.session.add(new_file)
    db.session.commit()

def add_parent_child(p_guid, c_guid):
    pc = ParentChild(parent_guid=p_guid, child_guid=c_guid)
    db.session.add(pc)
    db.session.commit()

def add_new_author(author_name):
    guid = str(uuid.uuid4())
    author = Author(name=author_name, GUID=guid)
    db.session.add(author)
    db.session.commit()

def query_by_date_created(date):
    dagrs = DAGR.query.filter_by(date_created=date).all()

    return dagrs

def query_by_date_modified(date):
    dagrs = DAGR.query.filter_by(date_modified=date).all()

    return dagrs

def query_by_type(ftype):
    dagrs = DAGR.query.filter_by(file_type=ftype).all()

    return dagrs

def query_by_annotations(annotes):
    dagrs = DAGR.query.filter(DAGR.annotations.like("%"+annotes+"%")).all()

    return dagrs

def query_by_name(file_name):
    dagrs = DAGR.query.filter(DAGR.name.like("%"+file_name+"%")).all()

    return dagrs

def query_by_author(name):
    guid = Author.query.filter_by(name=name).first().getGUID()

    dagrs = DAGR.query.filter_by(owner=guid).all()

    return dagrs

def has_parent(guid):
    return ParentChild.query.filter_by(child_guid=guid).all() != []

def has_child(guid):
    children = ParentChild.query.filter_by(parent_guid=guid).join(DAGR, ParentChild.child_guid==DAGR.GUID).filter(DAGR.file_type=="DAGR").all()
    return children != []

def orphan_report():
    all_dagrs = DAGR.query.all()
    orphan_func = lambda e: not has_parent(e.getGUID())
    return filter(orphan_func, all_dagrs)

def sterile_report():
    all_dagrs = DAGR.query.all()
    child_func = lambda e: not has_child(e.getGUID())
    return filter(child_func, all_dagrs)

def time_range(start_date, end_date):
    return DAGR.query.filter(DAGR.date_created >= start_date, DAGR.date_created <= end_date).all()

def reach(levels, initial):
    # - -> Up (ancestors)
    # + -> Down (descendants)
    step = 1 if levels > 0 else -1

    dagrs = [[initial]]
    for i in range(0, levels, step):
        for d in dagrs[len(dagrs) - 1]:
            if step < 1:
                q = ParentChild.query.filter_by(parent_guid=d).all()
                q = map(lambda x: x.getChildGUID(), q)
                dagrs.append(q)
            else:
                q = ParentChild.query.filter_by(child_guid=d).all()
                q = map(lambda x: x.getParentGUID(), q)
                dagrs.append(q)
    flat = list(set(reduce(lambda a, e: a + e, dagrs)))

    return map(lambda x: DAGR.query.filter_by(GUID=x).first(), flat)

def get_ancestors(initial):
    dagr = initial
    ancestors = []
    while has_parent(dagr):
        ancest = ParentChild.query.filter_by(child_guid=dagr).first().getParentGUID()
        ancestors.append(ancest)
        dagr = ancest

    return map(lambda x: DAGR.query.filter_by(GUID=x).first(), ancestors)

def get_descendants(initial):

    immediate_desc = map(lambda x: x.getChildGUID(), ParentChild.query.filter_by(parent_guid=initial).all())


    desc = []

    if DAGR.query.filter_by(GUID=initial).first().getType() == 'DAGR' or DAGR.query.filter_by(GUID=initial).first().getType() == 'HTML':
        immediate_desc = map(lambda x: x.getChildGUID(), ParentChild.query.filter_by(parent_guid=initial).all())
    else:
        immediate_desc = [initial]

    desc += immediate_desc

    # further = reduce(lambda a, e: get_descendants(e), immediate_desc, [])

    for f in immediate_desc:
        if f != initial:
            desc += get_descendants(f)

    if initial in desc:
        desc.remove(initial)

    return desc

    # return (map(lambda x: DAGR.query.filter_by(GUID=x).first(), immediate_desc))

"""
---------------------------Section for HTML Parsing---------------------------
"""

def parse_html(url, dagr_name):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    soup.prettify()
    for anchor in soup.findAll('a', href=True):
        if anchor['href'][:4] == 'http':
            filename = anchor['href']
            file_annotations = 'Link Parsed from ' + url
            file_type='HTML'
            if DAGR.query.filter_by(name=filename).all() == []:
                add_file_to_dagr(dagr_name=dagr_name, file_name=filename, file_annotations=file_annotations, file_type=file_type)

def parse_img(url, dagr_name):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    soup.prettify()
    for anchor in soup.findAll('img'):
        filename = anchor['src']
        file_annotations = "Image Parsed from " + url
        file_type = "Image"
        if DAGR.query.filter_by(name=filename).all() == []:
            add_file_to_dagr(dagr_name=dagr_name, file_name=filename, file_annotations=file_annotations, file_type=file_type)

"""
----------------------------Section for Bulk Upload----------------------------
"""

def bulk_upload(rootDir, author_name):
    # rootDir = '/Users/zach/Documents/Fall17/424/project/bulk_upload'
    # rootDir = '/Users/zach'
    parent = "new"
    visited = []
    for dirName, subdirList, fileList in os.walk(rootDir):

        dagr_name = dirName.split('/')[-1]

        if dagr_name not in visited:
            if parent != "new":
                parent = dirName.split('/')[-2]

            new_dagr(dagr_name=dagr_name, dagr_annotations="Bulk Upload", parent_dagr=parent, author_name=author_name)
            visited.insert(0,dagr_name)
            parent = dagr_name

        for fname in fileList:

            ft = magic.from_file(dirName + '/' + fname)
            if ft != 'empty':
                if DAGR.query.filter_by(name=fname).all() == []:
                    add_file_to_dagr(dagr_name=parent, file_name=fname, file_annotations="Bulk Upload File", file_type=ft, author_name=author_name)
                else:
                    ds = DAGR.query.filter_by(name=fname).all()
                    already_added = False
                    for d in ds:
                        parente = ParentChild.query.filter_by(child_guid=d.getGUID()).first()
                        if parente is not None:
                            if DAGR.query.filter_by(GUID=parente.parent_guid).first().getName() == parente:
                                already_added = True
                    if not already_added:
                        add_file_to_dagr(dagr_name=parent, file_name=fname, file_annotations="Bulk Upload File", file_type=ft, author_name=author_name)

"""
------------------------------Section for Server------------------------------
"""

@app.route("/")
def root_view():
    header = "CMSC424 - MMDA - Welcome to my Multi-Media Data Aggregator."
    return render_template('index.html',title=header)

@app.route("/makeDagr")
def create_dagr_view():
    header = "CMSC424 - MMDA - Create A New DAGR"

    names = reduce((lambda a, e: a + [e.getName()]), DAGR.query.filter_by(file_type="DAGR").all(), []) + ['new']

    authors = map(lambda x: x.getName(), Author.query.all()) + ['new']

    return render_template('makeDagr.html',title=header, dagr_list=names, author_list=authors)

@app.route("/makeDagr", methods=['POST'])
def insert_new_dagr():
    name = request.form['DAGR Name']
    annotations = request.form['Annotations']
    topic = request.form['topic']

    author = request.form['author']

    if author == "new":
        author = request.form['author-name']

    new_dagr(name, annotations, topic, author_name=author)

    names = reduce((lambda a, e: a + [e.getName()]),DAGR.query.filter_by(file_type="DAGR").all(), []) + ['new']

    header = "CMSC424 - MMDA - Create A New DAGR"
    return render_template('makeDagr.html',title=header, dagr_list=names)

@app.route("/bulk")
def bulk_view():
    header = "CMSC424 - MMDA - Bulk Upload"

    authors = map(lambda x: x.getName(), Author.query.all()) + ['new']

    return render_template('bulk.html', title=header, author_list=authors)

@app.route("/bulk", methods=['POST'])
def bulk_upload_view():
    header = "CMSC424 - MMDA - Bulk Upload"

    path = request.form['path']

    author = request.form['authors']

    if author == "new":
        author = request.form['author-name']

    bulk_upload(path, author)

    return render_template('bulk_complete.html', title=header)

@app.route("/upload")
def upload_view():
    header = "CMSC424 - MMDA - Upload File to DAGR"

    names = reduce((lambda a, e: a + [e.getName()]), DAGR.query.filter_by(file_type="DAGR").all(), []) + ['new']

    authors = map(lambda x: x.getName(), Author.query.all()) + ['new']

    return render_template('upload.html',title=header, dagr_list=names, author_list=authors)

@app.route("/upload", methods=['POST'])
def file_get():
    text = request.form['file']

    d_name = request.form['topic']

    annotations = request.form['file-annotations']

    author = request.form['author']

    if author == "new":
        author = request.form['author-name']

    add_file_to_dagr(dagr_name=d_name, file_name=text, file_annotations=annotations, author_name=author)

    parse_html(url=text, dagr_name=text)
    parse_img(url=text, dagr_name=text)

    header = "CMSC424 - MMDA - Upload File to DAGR"
    names = reduce((lambda a, e: a + [e.getName()]), DAGR.query.filter_by(file_type="DAGR").all(), []) + ['new']
    return render_template('upload.html',title=header, dagr_list=names)

@app.route("/reports")
def report_overview():
    header = "CMSC424 - MMDA - DAGR Reports"
    return render_template('reports.html', title=header)

@app.route("/metadata")
def metadata_report_view():
    header = "CMSC424 - MMDA - DAGR Reports"
    authors = map(lambda x: x.getName(), Author.query.all())

    types = reduce(lambda a, e: a + [e.getType()] if e.getType() not in a else a, DAGR.query.all(), []) + ['all']

    return render_template('metadata.html', title=header, author_list=authors, type_list=types)

@app.route("/metadata", methods=['POST'])
def metadata_report_generator():

    if 'date' in request.form.keys():
        date = request.form['date']
        dagrs = query_by_date_created(date)

        file_type = request.form['types']

        if file_type != "all":
            dagrs = filter(lambda x: DAGR.query.filter_by(GUID=x.getGUID()).first().getType() == file_type, dagrs)

        header = "CMSC424 - MMDA - Date Query: " + date

        return render_template('report.html', title=header, dagrs=dagrs)
    elif 'authors' in request.form.keys():
        author_name = request.form['authors']

        dagrs = query_by_author(author_name)

        file_type = request.form['types']

        if file_type != "all":
            dagrs = filter(lambda x: DAGR.query.filter_by(GUID=x.getGUID()).first().getType() == file_type, dagrs)

        header = "CMSC424 - MMDA - Author Query: " + author_name

        return render_template('report.html', title=header, dagrs=dagrs)
    elif 'types' in request.form.keys() and len(request.form.keys()) == 2:
        file_type = request.form['types']
        dagrs = query_by_type(ftype=file_type)

        header = "CMSC424 - MMDA - Type Query: " + file_type

        return render_template('report.html', title=header, dagrs=dagrs)
    elif 'annotations' in request.form.keys():
        annotations = request.form['annotations']
        dagrs = query_by_annotations(annotes=annotations)

        file_type = request.form['types']

        if file_type != "all":
            dagrs = filter(lambda x: DAGR.query.filter_by(GUID=x.getGUID()).first().getType() == file_type, dagrs)

        header = "CMSC424 - MMDA - Annotation Query: " + annotations

        return render_template('report.html', title=header, dagrs=dagrs)
    elif 'name' in request.form.keys():
        file_name = request.form['name']
        dagrs = query_by_name(file_name=file_name)

        file_type = request.form['types']

        if file_type != "all":
            dagrs = filter(lambda x: DAGR.query.filter_by(GUID=x.getGUID()).first().getType() == file_type, dagrs)

        header = "CMSC424 - MMDA - Name Query: " + file_name

        return render_template('report.html', title=header, dagrs=dagrs)

    else:
        header = "CMSC424 - MMDA - DAGR Reports"
        authors = map(lambda x: x.getName(), Author.query.all())

        types = reduce(lambda a, e: a + [e.getType()] if e.getType() not in a else a, DAGR.query.all(), [])

        return render_template('metadata.html', title=header, author_list=authors, type_list=types)

@app.route("/orphanreport")
def orphan_view():
    header = "CMSC424 - MMDA - Orphan Report"

    types = reduce(lambda a, e: a + [e.getType()] if e.getType() not in a else a, DAGR.query.all(), []) + ['all']

    return render_template('orphanreport.html', title=header, type_list=types)

@app.route("/orphanreport", methods=['POST'])
def orphan_report_generator():
    header = "CMSC424 - MMDA - Orphan Report"

    file_type = request.form['types']

    dagrs = orphan_report();

    if file_type != "all":
        dagrs = filter(lambda x: DAGR.query.filter_by(GUID=x.getGUID()).first().getType() == file_type, dagrs)

    return render_template('report.html', title=header, dagrs=dagrs)

@app.route("/sterilereport")
def sterile_view():
    header = "CMSC424 - MMDA - Sterile Report"

    types = reduce(lambda a, e: a + [e.getType()] if e.getType() not in a else a, DAGR.query.all(), []) + ['all']

    return render_template('sterilereport.html', title=header, type_list=types)

@app.route("/sterilereport", methods=['POST'])
def sterile_report_generator():
    header = "CMSC424 - MMDA - Sterile Report"

    file_type = request.form['types']

    dagrs = sterile_report();

    if file_type != "all":
        dagrs = filter(lambda x: DAGR.query.filter_by(GUID=x.getGUID()).first().getType() == file_type, dagrs)

    return render_template('report.html', title=header, dagrs=dagrs)

@app.route("/timerange")
def time_range_view():
    header = "CMSC424 - MMDA - Time-Range Query"

    return render_template('timerange.html', title=header)

@app.route("/timerange", methods=['POST'])
def generate_time_range_report():
    header = "CMSC424 - MMDA - Time-Range Query"

    date_from = request.form['date-from']
    date_to = request.form['date-to']

    dagrs = time_range(date_from, date_to)

    header += (": " + date_from + "->" + date_to)

    return render_template('report.html', title=header, dagrs=dagrs)

@app.route("/reach")
def reach_view():
    header = "CMSC424 - MMDA - Reach Query"

    dagrs_and_files = DAGR.query.all()
    names = map(lambda x: x.getName(), dagrs_and_files)

    directions = ['Up', 'Down']
    levels = [i for i in range(1, len(dagrs_and_files) + 1)]

    return render_template('reach.html', title=header, dagrs=names, dirs=directions, levels=levels)

@app.route("/reach", methods=['POST'])
def generate_reach():
    header = "CMSC424 - MMDA - Reach Query"

    start = request.form['start-dagr-file']
    direction = request.form['direction']

    level = int(request.form['level']) if direction == 'Up' else -(int(request.form['level']))

    start_guid = DAGR.query.filter_by(name=start).first().getGUID()

    dagrs = reach(level, start_guid)

    dagrs = filter(lambda x: x is not None, dagrs)

    return render_template('report.html', title=header, dagrs=dagrs)

@app.route("/dagrdelete")
def delete_view():
    header = "CMSC424 - MMDA - DAGR Deletion"

    dagrs_and_files = DAGR.query.all()

    return render_template('dagrdelete.html', title=header, dagrs=dagrs_and_files)

@app.route("/dagrdelete", methods=['POST'])
def confirm_ancestors():
    header = "CMSC424 - MMDA - DAGR Deletion"
    prompt = "Ancestor DAGRs Affected"

    selected = request.form.keys()[0]

    ancestors = get_ancestors(selected)

    return render_template('ancestordelete.html', title=header, dagrs=ancestors, dagr=selected)

@app.route("/dagrdeleteconfirm", methods=['POST'])
def prompt_descendants():
    header = "CMSC424 - MMDA - DAGR Deletion"
    prompt = "Delete Descendant DAGRs"

    selected = request.form.keys()[0]

    ParentChild.query.filter_by(child_guid=selected).delete()
    db.session.commit()

    descendants = get_descendants(selected)

    descendants = map(lambda x: DAGR.query.filter_by(GUID=x).first(), descendants)

    DAGR.query.filter_by(GUID=selected).delete()
    db.session.commit()

    return render_template('descendantdelete.html', title=header, dagrs=descendants, prompt=prompt, dagr_guid=selected)

@app.route("/descendantdeleteshallow", methods=['POST'])
def shallow_delete():
    header = "CMSC424 - MMDA - DAGR Deletion"

    guid = request.form.keys()[0]

    ParentChild.query.filter_by(parent_guid=guid).delete()
    db.session.commit()

    return render_template('deletecomplete.html', title=header)

@app.route("/descendantdeletedeep", methods=['POST'])
def deep_delete():
    return

@app.route("/reportview", methods=['POST'])
def report_view():
    header = "CMSC424 - MMDA - DAGR Inspection"

    guid = request.form.keys()[0]

    dagr = DAGR.query.filter_by(GUID=guid).first()

    ancestors = get_ancestors(guid)

    descendants = get_descendants(guid)

    descendants = map(lambda x: DAGR.query.filter_by(GUID=x).first(), descendants)

    return render_template('reportview.html', title=header, dagr=dagr, ancestors=ancestors, descendants=descendants)

if __name__ == "__main__":
    app.run(debug=True)
