from simulux.disks import Disks
from lib.utils import jsonify

# Global disks var to use in all the tests
disks = Disks()

def test_init():
    '''
    Test default load of the Disks class
    '''
    try:
        disks = Disks()
    except Exception as e:
        print "Exception raised: %s" % (e)
        assert False
    assert True

def test_get_childrens_path():
    '''
    Test that we can fetch 1st level of children of a path
    '''
    childrens = disks.get_childrens_path('/')
    childrens.sort()

    expected = [ unicode(i) for i in [
        '/bin', '/boot', '/dev', '/proc', '/home', '/root', '/sbin', 
        '/var', '/etc', '/lost+found', '/lib', '/lib64', '/opt', '/tmp',
        '/mnt', '/sys', '/usr'
    ]]
    expected.sort()
    assert childrens == expected

def test_get_parent_path():
    '''
    Test that we can fetch the parent path
    '''
    parent = disks.get_parent_path('/')
    assert parent == unicode('/')
    parent = disks.get_parent_path('/etc/hosts')
    assert parent == unicode('/etc')
    parent = disks.get_parent_path('/some/random/path')
    assert parent == unicode('/some/random')

def test_get_details_of_mount_point():
    '''
    Test we can fetch the details of a mount point folder
    '''
    details = disks.get_details('/')
    expected = {
        'mount': True,
        'size': 1000000,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)

def test_get_details_of_good_file():
    '''
    Test we can fetch the details of a good file
    '''
    details = disks.get_details('/etc/hosts')
    expected = {
        'filetype': 'file',
        'size': 11,
        'owner': 'root',
        'group': 'root',
        'mode': 644
    }
    assert jsonify(details) == jsonify(expected)
    details = disks.get_details('/etc')
    expected = {
        'filetype': 'folder',
        'size': 1111,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)

def test_get_details_of_bad_file():
    '''
    Test we can fetch the details of a bad file
    '''
    details = disks.get_details('/some/random/path')
    expected = {}
    assert jsonify(details) == jsonify(expected)

def test_add_new_file():
    '''
    Test we can add a new file and the size get propagated
    '''
    disks.add_file('/etc/new_file', size=1000)
    details = disks.get_details('/etc/new_file')
    expected = {
        'size': 1000,
        'owner': 'root',
        'group': 'root',
        'filetype': 'file',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)
    details = disks.get_details('/etc')
    expected = {
        'filetype': 'folder',
        'size': 2111,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)
    details = disks.get_details('/')
    expected = {
        'mount': True,
        'size': 1001000,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)

def test_update_file():
    '''
    Test we can update an existing file and the size get propagated
    '''
    disks.update_file('/etc/new_file', size=5000, mode=644, owner='foo', group='bar')
    details = disks.get_details('/etc/new_file')
    expected = {
        'size': 5000,
        'owner': 'foo',
        'group': 'bar',
        'filetype': 'file',
        'mode': 644
    }
    assert jsonify(details) == jsonify(expected)
    details = disks.get_details('/etc')
    expected = {
        'filetype': 'folder',
        'size': 6111,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)
    details = disks.get_details('/')
    expected = {
        'mount': True,
        'size': 1005000,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)

def test_remove_file():
    '''
    Test we can remove a file and get the size propagated
    '''
    disks.remove_file('/etc/new_file')
    details = disks.get_details('/etc/new_file')
    expected = {}
    assert jsonify(details) == jsonify(expected)
    details = disks.get_details('/etc')
    expected = {
        'filetype': 'folder',
        'size': 1111,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)
    details = disks.get_details('/')
    expected = {
        'mount': True,
        'size': 1000000,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)

def test_remove_folder():
    '''
    Test folder removal - fail on non recursive
    '''
    disks.remove_file('/etc')
    details = disks.get_details('/etc')
    # Fail - not deleted
    expected = {
        'filetype': 'folder',
        'size': 1111,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)
    disks.remove_file('/etc', recursive=True)
    details = disks.get_details('/etc')
    # Fail - not deleted
    expected = {}
    assert jsonify(details) == jsonify(expected)
    details = disks.get_details('/')
    expected = {
        'mount': True,
        'size': 998889,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)

def test_remove_mount():
    '''
    Test mount point folder removal - fail
    '''
    disks.remove_file('/boot')
    details = disks.get_details('/boot')
    # Fail - not deleted
    expected = {
        'mount': True,
        'size': 1111,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)
    disks.remove_file('/boot', recursive=True)
    details = disks.get_details('/boot')
    # Fail - not deleted
    expected = {
        'mount': True,
        'size': 1111,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)
    details = disks.get_details('/')
    # Unchanged from previous test and not propagated since other mount point
    expected = {
        'mount': True,
        'size': 998889,
        'owner': 'root',
        'group': 'root',
        'mode': 755
    }
    assert jsonify(details) == jsonify(expected)