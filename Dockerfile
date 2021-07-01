FROM opensciencegrid/software-base:fresh
LABEL maintainer OSG Software <help@opensciencegrid.org>

RUN yum -y install epel-release && \
    yum -y install vim && \
    yum -y install mod_wsgi && \
    yum -y install python-pip

RUN pip install —upgrade setuptools && \
    pip install flask==0.12.4 requests==2.20.0

RUN mkdir -p /var/www/GeoIP-Redi/app
RUN chown apache:apache /var/www/GeoIP-Redi/app

ADD supervisor.conf /etc/supervisord.d/
ADD image-config.d/* /etc/osg/image-config.d/
