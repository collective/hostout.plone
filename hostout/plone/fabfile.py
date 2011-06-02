from fabric import api
from collective.hostout.hostout import  asbuildoutuser

def _fscopy(tgt, db='Data.fs', filestorage="var/filestorage"):
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


def fscopy(tgt, filestorage="Data.fs", filestorage_dir="var/filestorage"):
    "Move the Data.fs to tgt (must be on the same machine)"
    target = api.env.hostout.hostouts[tgt]
    towner = target.options['buildout-user']
    e = dict(filestorage=filestorage, towner=towner)

    # Assumes we're on the same machine for this to work
    assert target.options['host'] == api.env.hostout.options['host']

    api.env.hostout.fsbackup(filestorage, filestorage_dir)
    with api.cd(api.env.path):
        with asbuildoutuser():
            backup = "var/backups/%(filestorage)s" % e
            api.run("cp -R %(backup)s /tmp" % dict(backup=backup))
            api.run("chown -R %(towner)s /tmp/%(filestorage)s" % e)

    target.run("cp -fR /tmp/%(filestorage)s var/backups/%(filestorage)s" % e )
    target.run("rm -Rf /tmp/%(filestorage)s " % e )
    target.fsrestore(filestorage, filestorage_dir)

def blobcopy(tgt, blobstorage="blobstorage"):
    "Copy blobstorage to tgt buildout (must be on the same machine)"
    target = api.env.hostout.hostouts[tgt]
    towner = target.options['buildout-user']
    e = dict(blobstorage=blobstorage, towner=towner)

    # Assumes we're on the same machine for this to work
    assert target.options['host'] == api.env.hostout.options['host']

    with api.cd(api.env.path):
        with asbuildoutuser():
            api.run("cp -R var/%(blobstorage)s /tmp" % e)
            api.run("chown -R %(towner)s /tmp/%(blobstorage)s" % e)

    target.supervisorctl("stop all")
    target.run("cp -fR /tmp/%(blobstorage)s var/" % e )
    target.run("rm -Rf /tmp/%(blobstorage)s " % e )
    target.supervisorctl("start all")



def fsget(filestorage="Data.fs", filestorage_dir="var/filestorage"):
    """ download a database from teh remote server and overwrite the local """
    api.env.hostout.fsbackup(filestorage, filestorage_dir)
    db = filestorage
    with api.cd(api.env.path):
        with asbuildoutuser():
            api.get('var/backups/%(db)s'%locals())
            api.local('bin/repozo --recover -o %(filestorage_dir)s/%(db)s -r var/backups/%(filestorage)s' % locals())

def fsbackup(filestorage="Data.fs", filestorage_dir="var/filestorage"):
    hostout = api.env.hostout
    db = filestorage
    with api.cd(api.env.path):
        with asbuildoutuser():
            api.run('mkdir -p var/backups/%(db)s' % locals())
            api.run('bin/repozo --backup -f %(filestorage_dir)s/%(db)s --gzip -r var/backups/%(db)s' % locals())


def fsrestore(filestorage="Data.fs", filestorage_dir="var/filestorage"):
    hostout = api.env.hostout
    hostout.supervisorctl("stop all")
    with api.cd(api.env.path):
        with asbuildoutuser():
            api.run('bin/repozo --recover -o %(filestorage_dir)s/%(filestorage)s -r var/backups/%(filestorage)s' % locals())
    hostout.supervisorctl("start all")
    

def hotfix(url):
    """ Takes a url and will deploy that to your products directory. Don't forget to restart after """
    with api.cd(api.env.path+'/products'):
        with asbuildoutuser():
            #api.run("curl %s /tmp/hotfix.zip"%url)
            api.run("python -c \"import urllib; f=open('/tmp/hotfix.zip','w'); f.write(urllib.urlopen('%s').read()); f.close()\""%url)
            api.run("unzip /tmp/hotfix.zip")
            api.run('rm /tmp/hotfix.zip')
            #api.run("python2.6 -c \"import zipfile;import urllib;import StringIO; zipfile.ZipFile(StringIO.StringIO(urllib.urlopen('%s').read())).extractall()\""%url)
            
