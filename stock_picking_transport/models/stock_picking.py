# Copyright 2024 ArPol
# @author: Armand Polmard <armand@arpol.fr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
import datetime
import logging


class StockPicking(models.Model):
    _inherit = "stock.picking"

    car = fields.Char(string="Véhicule utilisé", store=True)
    conso_totale = fields.Float(string="Consommation de la collecte (L)", compute='_compute_conso', store=True)
    conso_vehicule = fields.Float(string="Consommation du véhicule (L/100km)", store=True)
    cout_transport_major = fields.Monetary(string="Coût de transport majoré (€)", compute='_compute_transportation_cost_majored', store=True)
    cout_transport_net = fields.Monetary(string="Coût de transport net (€)", compute='_compute_transportation_cost', store=True)
    duree_collecte = fields.Integer(string="Durée de la collecte (h)", store=True)
    distance_collecte = fields.Float(string="Distance du point de collecte (km)", store=True)
    duree_trajet = fields.Float(string="Durée du trajet (min)", store=True)
    frais_km = fields.Monetary(string="Frais kilométriques (€/km)", store=True)
    frais_peage = fields.Monetary(string="Frais de péages (€)", store=True)
    nb_ar = fields.Integer(string="Nombre d'aller-retours", store=True)
    nb_intervenants = fields.Integer(string="Nombre d'intervenants", store=True)
    prix_carburant = fields.Monetary(string="Prix du carburant", store=True)

    @api.constrains('conso_totale','prix_carburant','conso_vehicule')
    def _compute_transportation_cost(self):
        for record in self:
            res = record.conso_totale * record.prix_carburant + record.frais_peage
            record.cout_transport_net = res

    @api.constrains('frais_km','distance_collecte','conso_vehicule')
    def _compute_transportation_cost_majored(self):
        for record in self:
            res = record.frais_km * 2 * record.distance_collecte * record.nb_ar + record.frais_peage
            record.cout_transport_major = res

    @api.constrains('distance_collecte','nb_ar','conso_vehicule') 
    def _compute_conso(self):
        for record in self:
            res = 2 * record.distance_collecte * record.nb_ar * record.conso_vehicule / 100
            record.conso_totale = res


