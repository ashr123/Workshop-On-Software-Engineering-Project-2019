from django.db.models import Q

from store.models import BaseItemRule as m_BaseItemRule


class BaseItemRule:
    def __init__(self, model=None):
        if model != None:
            self._model = model
            return

    @property
    def pk(self):
        return self._model.pk

    @property
    def id(self):
        return self._model.pk

    @property
    def type(self):
        return self._model.type

    @property
    def parameter(self):
        return self._model.parameter

    def check(self, amount):
        if self.type == 'MAX' and amount > int(self.parameter):
            return False
        elif self.type == 'MIN' and amount < int(self.parameter):
            return False
        return True

    def update(self, item_dict):
        for field in self._model._meta.fields:
            if field.attname in item_dict.keys():
                setattr(self._model, field.attname, item_dict[field.attname])
        self._model.save()

    def delete(self):
        self._model.delete()


    @staticmethod
    def get_b_rule(rule_id):
        return BaseItemRule(model=m_BaseItemRule.objects.get(id=rule_id))

    @staticmethod
    def get_item_bi_rules(item_id):
        cir_models = m_BaseItemRule.objects.filter(item_id=item_id)
        return list(map(lambda cir_model: BaseItemRule(model=cir_model), list(cir_models)))
