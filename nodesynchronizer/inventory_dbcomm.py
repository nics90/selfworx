from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import sys
import os
import json
import pickle
from datetime import datetime
import subprocess


#################################### Create Table ############################################

# meta = MetaData()
# engine = create_engine('mysql://root:password@127.0.0.1/inventorydb')
# node_table = Table(
#                    'Node',meta,
#                    Column('node',String(200), primary_key=True),
#                    Column('fqdn',String(200), nullable=False),
#                    Column('ip',String(250)),
#                    Column('domain',String(250)),
#                    Column('operating_system',String(250)),
#                    Column('machine_type',String(250)),
#                    Column('machine_status',String(250)),
#                    Column('created',DateTime),
#                    Column('updated',DateTime)
#                    )
#
# meta.create_all(engine)

# meta = MetaData()
# engine = create_engine('mysql://root:password@127.0.0.1/selfworx_app')
# node_synched_table = Table(
#                    'NodeSynced',meta,
#                    Column('node',String(200), primary_key=True),
#                    Column('fqdn',String(200), nullable=False),
#                    Column('ip',String(250)),
#                    Column('operating_system',String(250)),
#                    Column('machine_type',String(250)),
#                    Column('status',String(250)),
#                    Column('created',DateTime),
#                    Column('updated',DateTime)
#                    )
#
# meta.create_all(engine)
###############################################################################################




##############################################################################################

Base = declarative_base()

class Node(Base):
    __tablename__ = "Node"
    node = Column(String(200), primary_key=True)
    fqdn = Column(String(200), nullable=False)
    ip = Column(String(250))
    domain = Column(String(250))
    operating_system = Column(String(250))
    machine_type = Column(String(250))
    created = Column(DateTime)
    updated = Column(DateTime)


    def __init__(self, node, fqdn, ip, domain, operating_system, machine_type, created, updated):
        self.node = node
        self.fqdn = fqdn
        self.ip = ip
        self.domain = domain
        self.operating_system = operating_system
        self.machine_type = machine_type
        self.created = created
        self.updated = updated


##############################################################################################

engine = create_engine('mysql://root:password@127.0.0.1/inventorydb')

conn = engine.connect()
res = conn.execute('select * from Node where created >= NOW() - INTERVAL 9420 MINUTE')

rows = []
for row in res:
   rows.append(row.node+","+row.fqdn+","+row.ip+","+row.operating_system+","+row.machine_type)

curr_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = "data/collected_rows_"+curr_timestamp

with open(filename,"w") as fo:
    fo.writelines("%s\n" % row for row in rows)

lines = []
with open(filename,"r") as fo:
    lines = [ line.rstrip() for line in fo.readlines() ]


engine2 = create_engine('mysql://root:password@127.0.0.1/selfworx_app')
conn2 = engine2.connect()

for line in lines:
    #print(line.split(','))
    split_line = line.split(',')
    node_name = split_line[0]
    check_node_list = subprocess.check_output("knife node list | grep linnode1",shell=True)
    print(check_node_list)
    query1 = "select * from NodeSynced where node='"+split_line[0]+"';"
    query2 = "insert into NodeSynced (node,fqdn,ip,operating_system,machine_type,status,created,updated) \
    VALUES ('"+split_line[0]+"','"+split_line[1]+"','"+split_line[2]+"','"+split_line[3]+"','"+split_line[4]+"','UNMANAGED',now(),now())"
    conn2.execute(query1)
    result1 = conn2.execute(query1)
    print(query1)
    print(result1)
