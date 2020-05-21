from odoo import models, fields, api


class GovernorateSelection(models.Model):
    _name = 'governorate_selection'

    name = fields.Char('Add New Governorate', required=True)


class CitySelection(models.Model):
    _name = 'city_selection'

    name = fields.Char('Add New City', required=True)


class MaterialSelection(models.Model):
    _name = 'material_selection'

    name = fields.Char('Add New Material', required=True)
    price = fields.Float('Add Price', required=True)


class ShadeSelection(models.Model):
    _name = 'shade_selection'

    name = fields.Char('Add New Shade', required=True)
