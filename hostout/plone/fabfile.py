from fabric import api
from hostout import asbuildoutuser

def fscopy(tgt, db='Data.fs', filestorage="var/filestorage"):
    "Not working yet"
    hostout = api.env.hostout
    tgt = hostout.hostouts[tgt]
    template = '%(user)s@%(host)s:%(path)s'
    dest = template % tgt.options
    #dest = '%(dest)s/%(db)s' % locals()
    destkey,_ = tgt.getIdentityKey()
    src = template % hostout.options
    #src = '%(src)s/%(db)s' % locals()
    srckey,_ = hostout.getIdentityKey()
    api.env.cwd =  api.env.path
    api.sudo('mkdir -p var/backups/%(db)s' % locals())
    api.sudo('bin/repozo --backup -f %(filestorage)s/%(db)s --gzip -r var/backups/%(db)s' % locals())
    pw = tgt.options['password']
    api.run('set RSYNC_PASSWORD=%(pw)s; rsync -r var/backups/%(db)s %(dest)s/var/backups/' % locals())
#    api.run('scp -r var/backups/%(db)s %(src)s/var/backups/' % locals())
    tgt.restore(db,filestorage)
    #api.local('scp -B -v -i %(srckey)s -i %(destkey)s %(src)s  Data.fs '%locals())
    #api.local('scp -B -v -i %(srckey)s -i %(destkey)s Data.fs %(dest)s   '%locals())
    #api.local('scp -B -v -i %(srckey)s -i %(destkey)s %(src)s  %(dest)s '%locals())

def fsget(filestorage="Data.fs", filestorage_dir="var/filestorage"):
    """ download a database from teh remote server and overwrite the local """
    api.env.hostout.fsbackup(filestorage, filestorage_dir)
    db = filestorage
    with cd(api.env.path):
        with asbuildoutuser:
            api.get('var/backups/%(db)s')
            api.local('bin/repozo --backup -f %(filestorage_dir)s/%(db)s --gzip -r var/backups/%(db)s' % locals())

def fsbackup(filestorage="Data.fs", filestorage_dir="var/filestorage"):
    hostout = api.env.hostout
    db = filestorage
    with cd(api.env.path):
        with asbuildoutuser:
            api.run('mkdir -p var/backups/%(db)s' % locals())
            api.run('bin/repozo --backup -f %(filestorage_dir)s/%(db)s --gzip -r var/backups/%(db)s' % locals())


def fsrestore(filestorage="Data.fs", filestorage_dir="var/filestorage"):
    hostout = api.env.hostout
    hostout.supervisorctl("stop all")
    with cd(api.env.path):
        with asbuildoutuser:
            api.run('bin/repozo --recover -o %(filestorage_dir)s/%(db)s -r var/backups/%(filestorage)s' % locals())
    hostout.supervisorctl("start all")
    
