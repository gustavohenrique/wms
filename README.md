WMS - Workflow Management System
================================

Sistema de workflow criado em 2009 utilizando django-grappelli, ExtJS3 e geraldo-report.
Devido à grande procura na lista django-brasil resolvi publicar no github.

*Atenção*
Código feio e sem testes utilizando versões antigas do django e extjs.


Instalação
----------

Instale o virtualenv e virtualenvwrapper.
<pre>
mkvirtualenv --no-site-packages wms
pip install -r requirements.txt
</pre>

*Atenção*
foi testado apenas em ambiente Linux (Fedora 16/17 e Ubuntu 12.04) com encoding utf-8


Uso
---

<pre>
workon wms
python manage.py syncdb
python manage.py runserver
</pre>

Para adicionar processos, passos e trabalhos, utilize a interface do admin:
http://localhost:8000/admin


Fique à vontade para contribuir com o projeto.
