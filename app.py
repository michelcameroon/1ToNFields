from flask import Flask, render_template, request, redirect, url_for
#from models2 import db, OneTb, NTb, get_table_info
from models2 import db, OneTb, NTb

from sqlalchemy import create_engine
from sqlalchemy .orm import sessionmaker


app = Flask(__name__)

#engine = create_engine('sqlite:///your_database.db')
#Session = sessionmaker(bind=engine)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    fieldNames = OneTb.get_field_names()
    print (fieldNames)
    fieldNamesNoIds = []
    for fieldName in fieldNames:
        if fieldName != 'id':
           fieldNamesNoIds.append(fieldName)
    print ('fieldNamesNoIds')
    print (fieldNamesNoIds)
    if request.method == 'POST':
        # Create a new 1Tb record
        table = OneTb.__tablename__
        data = {fieldNamesNoId: request.form[fieldNamesNoId] for fieldNamesNoId in fieldNamesNoIds}
        #insert_query = table.insert().values(**data)
        #insert_query = OneTb.insert().values(**data)
        new_record = OneTb(**data)
        db.session.add(new_record)
        '''
        db.session.execute(insert_query)

        name = request.form['name']
        new_record = OneTb(name=name)
        db.session.add(new_record)
        '''
        db.session.commit()

        #nrelations = NTb.query.all()
        #print ('nrelations')
        #print (nrelations)

        return redirect(url_for('index'))

    # Fetch all 1Tb records
    records = OneTb.query.all()

    nrelations = NTb.query.all()

    return render_template('index.html', records=records, nrelations=nrelations, fieldNamesNoIds=fieldNamesNoIds)

@app.route('/nrelations/<int:one_tb_id>', methods=['GET', 'POST'])
def nrelations(one_tb_id):
    fieldNames = NTb.get_field_names()
    print (fieldNames)
    fieldNamesNoIds = []
    for fieldName in fieldNames:
        if fieldName != 'id':
           fieldNamesNoIds.append(fieldName)
    print ('fieldNamesNoIds')
    print (fieldNamesNoIds)

    if request.method == 'POST':
        # Create a new nTb record
        data = {fieldNamesNoId: request.form[fieldNamesNoId] for fieldNamesNoId in fieldNamesNoIds}

        new_n_relation = NTb(**data)
        db.session.add(new_n_relation)

        '''
        description = request.form['description']
        new_n_relation = NTb(description=description, one_tb_id=one_tb_id)
        db.session.add(new_n_relation)
        '''
        db.session.commit()
        return redirect(url_for('index'))

    #table_info = get_table_info('nTb')
    #return render_template('nrelations.html', one_tb_id=one_tb_id, table_info=table_info, fieldNamesNoIds=fieldNamesNoIds )
    return render_template('nrelations.html', one_tb_id=one_tb_id, fieldNamesNoIds=fieldNamesNoIds )

if __name__ == '__main__':
    app.run(debug=True)
