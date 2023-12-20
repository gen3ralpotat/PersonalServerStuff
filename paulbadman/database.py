import dataset

__DB = dataset.connect('sqlite:///paulbadmandatabase.db')
ATTACHMENT_TABLE : dataset.Table = __DB['ATTACHMENTS']
