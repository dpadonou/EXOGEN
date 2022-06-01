import collections
import copy
import unittest

from history.Operation import Operation
from history.Story import Story


class StoryTest(unittest.TestCase):

    def setUp(self):
        self.nb_op: int = 20
        self.nb_var: int = 3
        self.nb_trans: int = 3
        self.serializable: bool = False
        self.type_histoire: str = "R"

        self._hist = Story(10, 3, 3, False, 'SAC')

    '''
        Tester si le nombre d'opérations contenues dans l'histoire générée
            est strictement égal au nombre d'opérations passé en paramètre.
            
        Faire le test sur 10 itération
    '''

    def test_generated_story_length(self):
        for i in range(0, 10):
            with self.subTest(i=i):
                hist = Story(self.nb_op, self.nb_var, self.nb_trans, self.serializable, self.type_histoire)
                self.assertEqual(self.nb_op, len(hist.operations))

    '''
        Tester si le nombre de commit contenues dans l'histoire générée
            est strictement égal au nombre de transactions passé en paramètre.

        Faire le test sur 10 itération
    '''

    def test_c_number(self):
        for i in range(0, 10):
            with self.subTest(i=i):
                hist = Story(self.nb_op, self.nb_var, self.nb_trans, self.serializable, self.type_histoire)
                self.assertEqual(
                    self.nb_trans,
                    sum(1 for x in hist.operations if x.op_type == "c")
                )

    '''
        Tester si le nombre de variables contenues dans l'histoire générée
            est strictement égal au nombre de variables passé en paramètre.

        Faire le test sur 10 itération
    '''

    def test_var_number(self):
        for i in range(0, 10):
            with self.subTest(i=i):
                var_list: [str] = []

                hist = Story(20, 3, 3, True, 'SAC')

                for index, ope in enumerate(hist.operations):
                    if ope.var not in var_list and ope.op_type != 'c':
                        var_list.append(ope.var)

                self.assertEqual(
                    self.nb_var,
                    len(var_list)
                )

    '''
        Tester si la methode set_story remplace bien le contenu de la l'histoire par l'histoire passée en paramètre.
    '''

    def test_set_story(self):
        hist = Story(20, 3, 3, False, 'SAC')
        # Verifier qu'une histoire a bien été générer au préalable, avec les critère passés en paramètre
        self.assertEqual(20, len(hist.operations))
        self.assertEqual(3, hist.var_nb)
        self.assertEqual(3, hist.trans_nb)

        op_list = [Operation('r', 1, 'x'), Operation('w', 2, 'y'), Operation('r', 1, 'y'), Operation('w', 1, 'x'),
                   Operation('c', 1, None), Operation('r', 2, 'x'), Operation('W', 2, 'x'), Operation('c', 2, None)]
        hist.create_story(op_list)
        # Verifier qu'une nouvelle histoire remplace l'ancienne et que les paramètres de l'histoire ont été mis à jour
        self.assertEqual(len(op_list), len(hist.operations))
        self.assertEqual(2, hist.var_nb)
        self.assertEqual(2, hist.trans_nb)

    '''
        Tester si la fonction reorganise ne modifie l'histoire qu'en cas de nécessité.  
    '''

    def test_reorganise(self):
        op_list = [Operation('r', 1, 'x'), Operation('w', 1, 'y'), Operation('r', 2, 'y'), Operation('c', 1, None),
                   Operation('c', 2, None), Operation('W', 2, 'x')]
        self._hist.create_story(copy.deepcopy(op_list))
        self._hist.reorganise()
        self.assertNotEqual(collections.Counter(op_list), collections.Counter(self._hist.operations))

        op_list_2 = [Operation('r', 1, 'x'), Operation('w', 1, 'y'), Operation('r', 2, 'y'), Operation('c', 1, None),
                     Operation('W', 2, 'x'), Operation('c', 2, None)]
        self._hist.create_story(op_list_2)
        self._hist.reorganise()
        self.assertEqual(collections.Counter(op_list_2), collections.Counter(self._hist.operations))

    '''
        Tester si la méthode de vérifiction de sérialisabilité fonctionne pour une histoire reconnue sérialisable.
        L'objectif étant de s'assurer que la méthode qui permet de déterminer le caractère acyclique d'une histoire est fiable
    '''

    def test_serializable(self):
        self._hist.create_story(
            [Operation('r', 1, 'x'), Operation('w', 1, 'y'), Operation('r', 2, 'y'), Operation('c', 1, None),
             Operation('W', 2, 'x'), Operation('c', 2, None)])
        self.assertTrue(self._hist.is_serializable())


if __name__ == '__main__':
    unittest.main()
