from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.analytics.analytics import EntryException,SalesSeries,SalesByJurisdiction,min_max_dates,OER,OERScores
from ops.analytics.analytics import RFM,DashboardCounts,DaysPerformance,RateCategories,RateItems,RateStores

class oldest_youngest_datetimes(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        super(oldest_youngest_datetimes,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        return {"range":min_max_dates(owner_id)},200

class sales_series(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("startdate",help="required field",required=True)
        self.parser.add_argument("enddate",help="required field",required=True)
        self.parser.add_argument("owner_id",help="required field",required=True)
        super(sales_series,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        startdate=data["startdate"]
        enddate=data["enddate"]
        owner_id=data["owner_id"]
        return SalesSeries(startdate,enddate,owner_id).defaultmatrix(),200

class sales_by_jurisdiction(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(sales_by_jurisdiction,self)
        
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        language_id=data["language_id"]
        return SalesByJurisdiction(owner_id,language_id).getmatrix(),200

class dashboard_counts(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(dashboard_counts,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        owner_id=data["owner_id"]
        d=DashboardCounts(owner_id,language_id)
        return d._execute(),200

class days_performance(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(days_performance,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        language_id=data["language_id"]
        days,pcs,values=DaysPerformance(owner_id,language_id).getmatrix()
        return {"days":days,"pcs":pcs,"values":values},200

class top_5_categories(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        super(top_5_categories,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        return RateCategories(owner_id).top5(),200

class top_10_items(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        super(top_10_items,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data['owner_id']
        return RateItems(owner_id).top10(),200

class rate_stores(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(rate_stores,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        language_id=data["language_id"]
        return RateStores(owner_id,language_id).top(),200

class rfm_tables(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        super(rfm_tables,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data['owner_id']
        r=RFM(owner_id)
        matrix=r.getmatrix()
        if matrix.empty:return None
        else:
            cuts=r.qcuts(matrix)
            columns,rows=r.vaporizetable(cuts.copy(deep=True))
            source,series=r.chartdata(cuts.copy(deep=True))
            names,scores=OERScores(owner_id).getscores()
            return {"rfm":{"rows":rows,"columns":columns,"chartsource":source,"series":series},
            "oer":{"names":names,"scores":scores}},200

class oer_scores(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        super(oer_scores,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        names,scores=OERScores(owner_id).getscores()
        oer={"names":names,"scores":scores}
        r=RFM(owner_id);matrix=r.getmatrix()
        if matrix.empty:rfm=None
        else:
            cuts=r.qcuts(matrix)
            columns,rows=r.vaporizetable(cuts.copy(deep=True))
            source,series=r.chartdata(cuts.copy(deep=True))
            rfm={"rows":rows,"columns":columns,"chartsource":source,"series":series}
        return {"oer":oer,"rfm":rfm},200

