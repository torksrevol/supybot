#!/usr/bin/env python

###
# Copyright (c) 2002, Jeremiah Fincher
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

from testsupport import *

class TopicTestCase(ChannelPluginTestCase, PluginDocumentation):
    plugins = ('Topic',)
    def testRemove(self):
        self.assertError('topic remove 1')
        _ = self.getMsg('topic add foo')
        _ = self.getMsg('topic add bar')
        _ = self.getMsg('topic add baz')
        self.assertError('topic remove 0')
        self.assertNotError('topic remove 3')
        self.assertNotError('topic remove 2')
        self.assertNotError('topic remove 1')
        self.assertError('topic remove 1')

    def testGet(self):
        self.assertError('topic get 1')
        _ = self.getMsg('topic add foo')
        _ = self.getMsg('topic add bar')
        _ = self.getMsg('topic add baz')
        self.assertRegexp('topic get 1', '^foo')
        self.assertError('topic get 0')

    def testAdd(self):
        m = self.getMsg('topic add foo')
        self.assertEqual(m.command, 'TOPIC')
        self.assertEqual(m.args[0], self.channel)
        self.assertEqual(m.args[1], 'foo (test)')
        m = self.getMsg('topic add bar')
        self.assertEqual(m.command, 'TOPIC')
        self.assertEqual(m.args[0], self.channel)

    def testChange(self):
        _ = self.getMsg('topic add foo')
        _ = self.getMsg('topic add bar')
        _ = self.getMsg('topic add baz')
        self.assertRegexp('topic change -1 s/baz/biff/',
                          r'foo.*bar.*biff')
        self.assertRegexp('topic change 2 s/bar/baz/',
                          r'foo.*baz.*biff')
        self.assertRegexp('topic change 1 s/foo/bar/',
                          r'bar.*baz.*biff')
        self.assertRegexp('topic change -2 s/baz/bazz/',
                          r'bar.*bazz.*biff')
        self.assertError('topic change 0 s/baz/biff/')

    def testConfig(self):
        try:
            conf.supybot.plugins.Topic.separator.setValue(' <==> ')
            _ = self.getMsg('topic add foo')
            m = self.getMsg('topic add bar')
            self.failUnless('<==>' in m.args[1])
        finally:
            default = conf.supybot.plugins.Topic.separator.default()
            conf.supybot.plugins.Topic.separator.setValue(default)

    def testReorder(self):
        _ = self.getMsg('topic add foo')
        _ = self.getMsg('topic add bar')
        _ = self.getMsg('topic add baz')
        self.assertRegexp('topic reorder 2 1 3', r'bar.*foo.*baz')
        self.assertRegexp('topic reorder 3 -2 1', r'baz.*foo.*bar')
        self.assertError('topic reorder 0 1 2')
        self.assertError('topic reorder 1 -2 2')
        self.assertError('topic reorder 1 2')
        self.assertError('topic reorder 2 3 4')
        self.assertError('topic reorder 1 2 2')
        self.assertError('topic reorder 1 1 2 3')
        _ = self.getMsg('topic remove 1')
        _ = self.getMsg('topic remove 1')
        self.assertError('topic reorder 1')
        _ = self.getMsg('topic remove 1')
        self.assertError('topic reorder 0')

    def testList(self):
        _ = self.getMsg('topic add foo')
        self.assertRegexp('topic list', '1: foo')
        _ = self.getMsg('topic add bar')
        self.assertRegexp('topic list', '1: foo .*2: bar')
        _ = self.getMsg('topic add baz')
        self.assertRegexp('topic list', '1: foo .* 2: bar .* and 3: baz')


# vim:set shiftwidth=4 tabstop=8 expandtab textwidth=78:

