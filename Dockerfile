FROM opensciencegrid/software-base:fresh
LABEL maintainer OSG Software <help@opensciencegrid.org>

RUN yum -y install epel-release && \
    yum -y install vim && \
    yum -y install mod_wsgi && \
    yum -y install python-pip

RUN python -m pip install --upgrade pip && \
    python -m pip install flask requests

RUN mkdir -p /var/www/GeoIP-Redi/app
RUN chown apache:apache /var/www/GeoIP-Redi/app

ADD supervisor.conf /etc/supervisord.d/
ADD image-config.d/* /etc/osg/image-config.d/
