
.. code:: ipython3

    %matplotlib inline

导出线和链中的数据
==================

.. code:: ipython3

    from catplot.ep_components.ep_canvas import EPCanvas
    from catplot.ep_components.ep_lines import ElementaryLine
    from catplot.ep_components.ep_chain import EPChain

创建两条线
----------

.. code:: ipython3

    line1 = ElementaryLine([0.0, 1.2, 0.7], n=2)  # 是数据少一点，这里n=2
    line2 = ElementaryLine([0.0, 0.5], n=2)

将\ ``line1``\ 中的数据导出到\ ``line1.csv``\ 中
------------------------------------------------

.. code:: ipython3

    line1.export("line1.csv")

.. code:: ipython3

    cat line1.csv


.. parsed-literal::

    
    
    
    
    
    


创建链
------

.. code:: ipython3

    chain = EPChain([line1, line2])

将\ ``chain``\ 中的数据导出到\ ``chain.csv``\ 中
------------------------------------------------

.. code:: ipython3

    chain.export("chain.csv")

.. code:: ipython3

    cat chain.csv


.. parsed-literal::

    
    
    
    
    
    
    
    
    
    
    
    

