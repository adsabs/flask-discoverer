import unittest
try:
  from flask.ext.discoverer import advertise
except ImportError:
  import sys
  sys.path.append('..')
  from flask_discoverer import advertise

class TestDecorator(unittest.TestCase):
  def setUp(self):
    def testfunction(a,b,c):
      '''docstring of testfunction'''
      return "{a}|{b}|{c}".format(a=a,b=b,c=c)
    self.testfunction = testfunction

  def tearDown(self):
    del self.testfunction

  def test_advertiseAttributes(self):
    '''
    Test advertising, but not actually setting, attributes of a function
    '''
    self.testfunction = advertise('thisattr')(self.testfunction)
    self.assertRaises(AttributeError,lambda: self.testfunction.thisattr)
    self.assertEqual(self.testfunction._advertised,['thisattr'])

    res = self.testfunction(1,2,3)
    self.assertEqual(res,'1|2|3')

    @advertise('decor1','decor2')
    def testfunction(a,b,c):
      return "{a}|{b}|{c}".format(a=a,b=b,c=c)

    self.assertRaises(AttributeError,lambda: testfunction.decor1)
    self.assertRaises(AttributeError,lambda: testfunction.decor2)
    self.assertItemsEqual(testfunction._advertised,['decor1','decor2'])

    res = testfunction(1,2,3)
    self.assertEqual(res,'1|2|3')    

  def test_setAttributes(self):
    '''
    Test setting attributes of a function with an explicit call to advertise()
    and with @advertise. Assert that the function code executes as expected after
    the operators.
    '''
    self.testfunction = advertise(thisattr='foo')(self.testfunction)
    self.assertEqual(self.testfunction.thisattr,'foo')
    self.assertEqual(self.testfunction._advertised,['thisattr'])

    self.testfunction = advertise(thisattr2='foo2')(self.testfunction)
    self.assertEqual(self.testfunction.thisattr,'foo')
    self.assertEqual(self.testfunction.thisattr2,'foo2')
    self.assertItemsEqual(self.testfunction._advertised,['thisattr','thisattr2'])

    res = self.testfunction(1,2,3)
    self.assertEqual(res,'1|2|3')

    @advertise(decor1='foo',decor2='bar')
    def testfunction(a,b,c):
      return "{a}|{b}|{c}".format(a=a,b=b,c=c)

    self.assertEqual(testfunction.decor1,'foo')
    self.assertEqual(testfunction.decor2,'bar')
    self.assertItemsEqual(testfunction._advertised,['decor1','decor2'])

    res = testfunction(1,2,3)
    self.assertEqual(res,'1|2|3')

if __name__=='__main__':
  unittest.main(verbosity=2)