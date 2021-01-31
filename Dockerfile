FROM opensciencegrid/software-base:fresh
LABEL maintainer OSG Software <help@opensciencegrid.org>

RUN yum -y install vim emacs && \
    yum -y install mod_wsgi && \
    yum -y install python-pip

RUN pip install flask requests

RUN mkdir -p /var/www/FLASKAPPS/GeoIP
RUN chown apache:apache /var/www/FLASKAPPS/GeoIP 

ADD supervisor.conf /etc/supervisord.d/
ADD image-config.d/* /etc/osg/image-config.d/
