FROM opensciencegrid/software-base:fresh
LABEL maintainer OSG Software <help@opensciencegrid.org>

RUN yum -y install epel-release && \
    yum -y install vim && \
    yum -y install httpd-devel && \
    yum -y install python3

RUN pip3 install flask requests mod_wsgi

RUN mkdir -p /var/www/GeoIP-Redi/app
RUN chown apache:apache /var/www/GeoIP-Redi/app

ADD supervisor.conf /etc/supervisord.d/
ADD image-config.d/* /etc/osg/image-config.d/
