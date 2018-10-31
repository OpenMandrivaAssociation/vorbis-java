%{?_javapackages_macros:%_javapackages_macros}
# Conditionals to help breaking vorbis-java-tika <-> tika dependency cycle
%bcond_with tika
Name:          vorbis-java
Version:       0.6
Release:       1.3
Summary:       Ogg and Vorbis toolkit for Java
Group:		Development/Java
License:       ASL 2.0
URL:           https://github.com/Gagravarr/VorbisJava
Source0:       https://github.com/Gagravarr/VorbisJava/archive/%{name}-%{version}.tar.gz

%if %{with tika}
BuildRequires: mvn(org.apache.tika:tika-core)
%endif
# test deps
BuildRequires: mvn(junit:junit)

BuildRequires: maven-local
BuildRequires: maven-surefire-provider-junit

BuildArch:     noarch

%description
This library is a pure Java, for working with Ogg and
Vorbis files.

%if %{with tika}
%package tika
Summary:       VorbisJava Apache Tika plugin

%description tika
This package contains Apache Tika plugin for Ogg,
Vorbis and FLAC.
%endif

%package tools
Summary:       VorbisJava Tools

%description tools
This package contains VorbisJava Ogg and Vorbis tools for Java.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n VorbisJava-%{name}-%{version}
find . -name "*.class" -delete
find . -name "*.jar" -delete

%if %{without tika}
%pom_disable_module tika
%endif

# disable embedded core copy
%pom_remove_plugin :maven-assembly-plugin tools

%pom_remove_plugin :maven-gpg-plugin parent
%pom_remove_plugin :maven-source-plugin parent
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions" parent

%build

%mvn_package :%{name} %{name}
%mvn_package :%{name}-parent %{name}
%mvn_package :%{name}-core %{name}
# Skip test @ random fails on arm builder
%mvn_build -s -f -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles-%{name}
%dir %{_javadir}/%{name}
%doc CHANGES.txt LICENSE.txt NOTICE.txt README.txt TODO.txt

%if %{with tika}
%files tika -f .mfiles-%{name}-tika
%doc LICENSE.txt NOTICE.txt
%endif

%files tools -f .mfiles-%{name}-tools
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Thu Sep 25 2014 gil cattaneo <puntogil@libero.it> 0.6-1
- update to 0.6

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 02 2013 gil cattaneo <puntogil@libero.it> 0.2-1
- initial rpm
