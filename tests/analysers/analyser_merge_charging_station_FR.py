# -*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Baptiste Lemoine 2023                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################
# import importlib
import unittest
from analysers.formatters.IRVEChecker import IRVE_checker


class Test(unittest.TestCase):
    def test_output_kw_bad_input(self):
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('bonjour'), '')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('0'), '')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances(''), '')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('Non applicable'), '')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('132456789'), '')

    def test_output_watts(self):
        # self.assertEqual(IRVE_checker.socket_output_find_correspondances('3600'), '3.6 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('3600'), '3.6 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('50000'), '50 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('400000'), '400 kW')

    def test_output_kw_round(self):
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('150'), '150 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('300'), '300 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('50'), '50 kW')

    def test_output_kw_float(self):
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('50.7'), '50.7 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('50.0'), '50 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('50.00'), '50 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('1.00'), '1 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('1.0'), '1 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('1'), '1 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('7.4'), '7.4 kW')
        self.assertEqual(IRVE_checker.socket_output_find_correspondances('3.6'), '3.6 kW')
