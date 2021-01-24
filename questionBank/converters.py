from werkzeug.routing import BaseConverter


class DictConverter(BaseConverter):
    def to_python(self, value):
        return_value = {}
        key_value_list = value.split(',')
        for key_value in key_value_list:
            key = key_value.split(':')[0].split("'")[1]
            value = key_value.split(':')[1].split("'")[1]
            return_value[key] = value
        return return_value

    # def to_url(self, value):
    #     pass


