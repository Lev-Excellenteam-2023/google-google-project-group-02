from data_class.file_data import *

files = FileData()


def test_file_name():
    index = files.free_index
    files.add_file('my_file', "i'm a big\nboy")
    assert files.data_dict[index][0] == 'my_file'


def test_simple_add_file_data():
    index = files.free_index
    files.add_file('google', 'Introduction to Networking\nIn the early days of computing, there were mainframe '
                             'computers. These computers were large and centrally located,\nusually in a very cold '
                             'and climate-controlled environment.')
    assert files.data_dict[index][1] == ['Introduction to Networking', 'In the early days of computing, there were '
                                                                       'mainframe computers. These computers were '
                                                                       'large and centrally located,', 'usually in a '
                                                                       'very cold and climate-controlled environment.']


def test_add_file_data_with_a_few_new_lines():
    index = files.free_index
    files.add_file('google', '1\n\nch01.qxd\n\n1/3/2001\n\n2\n\n9:44 AM\n\nChapter 1\n\nPage 2\n\n•\n\nIntroduction '
                             'to Networking and the OSI Model\n\nsend back to the mainframe. For this reason, '
                             'these terminals were often')
    assert files.data_dict[index][1] == ['1', 'ch01.qxd', '1/3/2001', '2', '9:44 AM', 'Chapter 1', 'Page 2', '•',
                                         'Introduction to Networking and the OSI Model',
                                         'send back to the mainframe. For this reason, these terminals were often']


def test_get_line():
    index = files.free_index
    files.add_file('arg', 'Technology started producing smarter terminals to decrease the load on\nthe mainframe. '
                          'When the personal computer (PC) became a reality in the late\n1980s, the paradigm began to '
                          'shift. PCs could connect to the mainframe in\nplace of the dumb terminals, '
                          'but more importantly, they could process data\non their own. The PC revolution began, '
                          'and the increasing importance of the\nhome and office computer was realized.')
    files.add_file('new_file', 'As more and more LANs became operational, it became necessary to\nlink these networks '
                               'together across floors, buildings, cities, and even countries; hence, '
                               'the introduction of the Wide Area Network, or WAN. A WAN is a\nmeans of connecting '
                               'LANs together across a distance boundary. Typical WAN\nconnectivity was accomplished '
                               'through phone lines.\nToday, computers throughout the world are connected through '
                               'WANs,')
    assert files.get_line(index, 3) == 'place of the dumb terminals, but more importantly, they could process data'
