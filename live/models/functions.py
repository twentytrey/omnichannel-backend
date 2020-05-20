def build_constraint(constrained,constraint,column,parent,parentcolumn):
    return """alter table {0} add constraint {1} foreign key({2})references {3}({4})on delete cascade""".format(constrained,constraint,column,parent,parentcolumn)
