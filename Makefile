DEBIAN_DIST=experimental
HSN2_COMPONENT=pcap-extract

PKG=hsn2-$(HSN2_COMPONENT)_$(HSN2_VER)-$(BUILD_NUMBER)_all
package: clean
	mkdir -p $(PKG)/opt/hsn2/pcap-extract
	mkdir -p $(PKG)/opt/hsn2/tcpxtract
	mkdir -p $(PKG)/etc/hsn2/
	mkdir -p $(PKG)/etc/init.d
	mkdir -p $(PKG)/DEBIAN
	cp *.py $(PKG)/opt/hsn2/pcap-extract/
	cp -r verifiers $(PKG)/opt/hsn2/pcap-extract/
	cp debian/initd $(PKG)/etc/init.d/hsn2-pcap-extract
	cp debian/pcap-extract.conf $(PKG)/etc/hsn2/pcap-extract.conf
	cp debian/tcpxtract.conf $(PKG)/etc/hsn2/tcpxtract.conf
	cp debian/control $(PKG)/DEBIAN
	cp debian/conffiles $(PKG)/DEBIAN
	cp debian/postrm $(PKG)/DEBIAN
	cp debian/postinst $(PKG)/DEBIAN
	sed -i "s/{VER}/${HSN2_VER}-${BUILD_NUMBER}/" $(PKG)/DEBIAN/control
	sed -i "s/{DEBIAN_DIST}/${DEBIAN_DIST}/" $(PKG)/DEBIAN/control
	fakeroot dpkg -b $(PKG)
	
clean:
	rm -rf $(PKG)