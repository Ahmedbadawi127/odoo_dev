# -*- coding: utf-8 -*-
from odoo import http

# class Lab(http.Controller):
#     @http.route('/lab/lab/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lab/lab/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lab.listing', {
#             'root': '/lab/lab',
#             'objects': http.request.env['lab.lab'].search([]),
#         })

#     @http.route('/lab/lab/objects/<model("lab.lab"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lab.object', {
#             'object': obj
#         })