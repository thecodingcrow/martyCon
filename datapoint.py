class Datapoint:
    uid = ""
    id_path = ""
    name = ""
    description = ""
    server_object_name = ""
    object_description = ""
    cov_increment = ""
    object_type = ""
    object_instance = ""
    cli_map_instance = ""

    def __init__(self, props={}):
        self.__set_props(**props)

    def __to_string(self):
        return '[DP ' + self.uid + ' ' + self.name + ']'

    def __str__(self):
        return self.__to_string()

    def __unicode__(self):
        return self.__to_string()

    def __repr__(self):
        return self.__to_string()

    def __set_props(self, uid="", id_path="", name="", description="", server_object_name="", object_description="", cov_increment="",
                    object_type="", object_instance="", cli_map_instance=""):
        self.uid = uid
        self.id_path = id_path
        self.name = name
        self.description = description
        self.server_object_name = server_object_name
        self.object_description = object_description
        self.cov_increment = cov_increment
        self.object_type = object_type
        self.object_instance = object_instance
        self.cli_map_instance = cli_map_instance
