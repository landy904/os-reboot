# -*- coding: utf-8 -*-

import os,shutil

print os.getcwd()
print os.chdir('D:/work/inbreak-check/test/')
print os.getcwd()
print os.listdir('.')
# print os.path.isdir('test')
print os.path.getsize('test.py')
print os.path.abspath('.')
fp = open('config.xml','w+')
seq = ["""<?xml version="1.0" encoding="UTF-8"?>
<domain xsi:schemaLocation="http://xmlns.oracle.com/weblogic/security/wls http://xmlns.oracle.com/weblogic/security/wls/1.0/wls.xsd h
ttp://xmlns.oracle.com/weblogic/domain http://xmlns.oracle.com/weblogic/1.0/domain.xsd http://xmlns.oracle.com/weblogic/security http
://xmlns.oracle.com/weblogic/1.0/security.xsd http://xmlns.oracle.com/weblogic/security/xacml http://xmlns.oracle.com/weblogic/securi
ty/xacml/1.0/xacml.xsd" xmlns="http://xmlns.oracle.com/weblogic/domain" xmlns:sec="http://xmlns.oracle.com/weblogic/security" xmlns:w
ls="http://xmlns.oracle.com/weblogic/security/wls" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <name>base_domain</name>
  <domain-version>10.3.6.0</domain-version>
  <security-configuration xmlns:xacml="http://xmlns.oracle.com/weblogic/security/xacml" xmlns:pas="http://xmlns.oracle.com/weblogic/s
ecurity/providers/passwordvalidator">
    <name>base_domain</name>
    <realm>
      <sec:authentication-provider xsi:type="wls:default-authenticatorType"/>
      <sec:authentication-provider xsi:type="wls:default-identity-asserterType">
        <sec:active-type>AuthenticatedUser</sec:active-type>
      </sec:authentication-provider>
      <sec:role-mapper xsi:type="xacml:xacml-role-mapperType"/>
      <sec:authorizer xsi:type="xacml:xacml-authorizerType"/>
      <sec:adjudicator xsi:type="wls:default-adjudicatorType"/>
      <sec:credential-mapper xsi:type="wls:default-credential-mapperType"/>
      <sec:cert-path-provider xsi:type="wls:web-logic-cert-path-providerType"/>
      <sec:cert-path-builder>WebLogicCertPathProvider</sec:cert-path-builder>
      <sec:name>myrealm</sec:name>
      <sec:password-validator xsi:type="pas:system-password-validatorType">
        <sec:name>SystemPasswordValidator</sec:name>
        <pas:min-password-length>8</pas:min-password-length>
                <pas:min-numeric-or-special-characters>1</pas:min-numeric-or-special-characters>
      </sec:password-validator>
    </realm>
    <default-realm>myrealm</default-realm>
    <credential-encrypted>{AES}3iANhSAX9YnSH8cO3oN9nBh7PNlTOR9VssZrokgH15CTdYrI/G/lfVpxVdowMfdnQNYcw5yVOlIKw4p0VCL4nuuudVaNQecXmD7GbG
UlD25ylZogpeWMFlZZ1hSDiPWB</credential-encrypted>
    <node-manager-username>KnDwIWyLFq</node-manager-username>
    <node-manager-password-encrypted>{AES}sLLO1VB0l90rKGaprzskH84RW0LIYychfxSm3hiNd2g=</node-manager-password-encrypted>
  </security-configuration>
    <server>
    <name>AdminServer</name>
    <listen-port>7002</listen-port>
    <listen-address>192.168.163.227</listen-address>
  </server>
  <server>
    <name>s1</name>
    <listen-port>7003</listen-port>
    <listen-address>192.168.163.227</listen-address>
  </server>
  <server>
    <name>s2</name>
    <listen-port>7003</listen-port>
    <listen-address>192.168.131.65</listen-address>
  </server>
  <server>
    <name>s3</name>
    <listen-port>7003</listen-port>
    <listen-address>192.168.131.66</listen-address>
  </server>
  <production-mode-enabled>true</production-mode-enabled>
  <embedded-ldap>
      <name>base_domain</name>
    <credential-encrypted>{AES}CBoPitqJD8dZqp/YvoB2rDvb+/uxndCCEvUU4P33r01OkfSM3Hd44jBDO64Od6/e</credential-encrypted>
  </embedded-ldap>
  <configuration-version>10.3.6.0</configuration-version>
  <admin-server-name>AdminServer</admin-server-name>
</domain>""",'\ntest',"""\nsjfkalsjfdlksajfdlkjsaf"""]
fp.writelines(seq)