WFW
===

CLI for WorkFlowy inspired by WWW:WorkFlowy_

WorkFlowy does not maintain an external API, so the cli can break anytime. **Do not use it for anything mission critical.**

Installation
------------

Please note that the package supports **Python 2.7** only.

Install it using pip
::

    pip install wfw


Configuration
-------------

Configure the tool using a configuration file. The name of the file have to be .wfwrc and it is must be located
in the home directory. **If the following options are not set properly, connecting to the server is not possible.**

Sample configuration
~~~~~~~~~~~~~~~~~~~~

/home/user/.wfwrc
::

    [user]
    email: name@server.com
    password: secretpass

Commands
--------

wfw add <parent-item> <new-item>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add new item to list.

| parent-item: parent of the new item
| new-item: new item's text

``wfw add "My list" "Shopping list"``

``wfw add places home``

wfw export <filename>
~~~~~~~~~~~~~~~~~~~~~

Export the list to file. The output file can be imported to hnb.

filename: path to file, default: tree.exported in current directory

``wfw export``

``wfw export my-pretty-file``

wfw fetch
~~~~~~~~~

Fetch list from WorkFlowy server.

``wfw fetch``

wfw find <pattern>
~~~~~~~~~~~~~~~~~~

Find items using pattern matching.

pattern: pattern that matches the item

``wfw find TODO``

``wfw find ba*``

wfw rm <parent-item> <deleted-item>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove item from list.

| parent-item: parent of the deleted item
| deleted-item: deleted item's text

``wfw rm "My list" TODOs``

``wfw rm TODO shopping``

wfw show --root <root> <depth>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prints list until given depth.

| root: text of the root item, default: root of tree
| depth: height of tree to be printed, default: 1

``wfw show``

``wfw show 2``

``wfw show --root personal 3``

wfw tag <tag-to-find>
~~~~~~~~~~~~~~~~~~~~~

Find items containing the given tag.

tag-to-find: name of tag to find

``wfw tag @work``

``wfw tag "#ThisWeek"``

Author
======

Noemi Vanyi

.. _WWW:WorkFlowy: https://github.com/cotto/www-workflowy/
