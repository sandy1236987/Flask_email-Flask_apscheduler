from marshmallow import Schema, fields
class PostPunchRequest(Schema):
    PO_Number = fields.Str(doc = "使用者員編",required = True)
    Account = fields.Str(doc = "使用者email",required = True)
    Passwd = fields.Str(doc = "使用者密碼",required = True)
    Team = fields.Str(doc = "使用者部門",required = True)
    Dept = fields.Str(doc = "使用者職稱",required = True)
    PO_Name = fields.Str(doc = "使用者姓名",required = True)

class PatchPunchRequest(Schema):
    PO_Number = fields.Str(doc = "使用者員編",required = True)
    Account = fields.Str(doc = "使用者email",required = True)
    Passwd = fields.Str(doc = "使用者密碼",required = True)
    Team = fields.Str(doc = "使用者部門",required = True)
    Dept = fields.Str(doc = "使用者職稱",required = True)
    PO_Name = fields.Str(doc = "使用者姓名",required = True)


    