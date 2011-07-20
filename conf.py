from ConfigParser import RawConfigParser, NoOptionError

HAROLD_PREFIX = "harold"
IDENT_SECTION_NAME = HAROLD_PREFIX + ":" + "ident"
IRC_SECTION_NAME = HAROLD_PREFIX + ":" + "irc"
JABBER_SECTION_NAME = HAROLD_PREFIX + ":" + "jabber"
HTTP_SECTION_NAME = HAROLD_PREFIX + ":" + "http"
REPOSITORY_PREFIX = HAROLD_PREFIX + ":" + "repository" + ":"


class _ConfigStub(object):
    pass


class HaroldConfiguration(object):
    def __init__(self, filenames):
        parser = RawConfigParser({
            'password': None,
            'use_ssl': False,
            'branch_filters': [],
            'format': ('%(author)s committed %(commit_id)s (%(url)s) to ' +
                       '%(repository)s: %(summary)s')
        })
        parser.read(filenames)

        # ident
        if parser.has_section(IDENT_SECTION_NAME):
            self.ident = _ConfigStub()
            self.ident.user = parser.get(IDENT_SECTION_NAME, "user")
            self.ident.port = parser.getint(IDENT_SECTION_NAME, "port")

        # read the basic IRC configuration
        if parser.has_section(IRC_SECTION_NAME):
            self.irc = _ConfigStub()
            self.irc.host = parser.get(IRC_SECTION_NAME, "host")
            self.irc.port = parser.getint(IRC_SECTION_NAME, "port")
            self.irc.use_ssl = parser.getboolean(IRC_SECTION_NAME, "use_ssl")
            self.irc.nick = parser.get(IRC_SECTION_NAME, "nick")
            self.irc.password = parser.get(IRC_SECTION_NAME, "password")

        # jabber configuration
        if parser.has_section(JABBER_SECTION_NAME):
            self.jabber = _ConfigStub()
            self.jabber.host = parser.get(JABBER_SECTION_NAME, "host")
            self.jabber.port = parser.getint(JABBER_SECTION_NAME, "port")
            self.jabber.id = parser.get(JABBER_SECTION_NAME, "id")
            self.jabber.password = parser.get(JABBER_SECTION_NAME,
                                              "password")
            recipients = parser.get(JABBER_SECTION_NAME, "recipients")
            self.jabber.recipients = [x.strip() for x in
                                      recipients.split(',') if x]

        # read the basic HTTP configuration
        self.http = _ConfigStub()
        self.http.port = parser.getint(HTTP_SECTION_NAME, "port")
        self.http.secret = parser.get(HTTP_SECTION_NAME, "secret")

        # read the repositories
        self.repositories = []
        self.repositories_by_name = {}
        self.channels = set()
        for section in parser.sections():
            if not section.startswith(REPOSITORY_PREFIX):
                continue

            repository = _ConfigStub()
            repository.name = section[len(REPOSITORY_PREFIX):]
            repository.channel = parser.get(section, "channel")
            repository.format = parser.get(section, "format")

            # parse the branch filters
            try:
                branch_list = parser.get(section, "branch_filters")
                repository.branches = [x.strip() for x in
                                       branch_list.split(',') if x]
            except NoOptionError:
                repository.branches = []

            self.repositories.append(repository)
            self.repositories_by_name[repository.name] = repository
            self.channels.add(repository.channel)