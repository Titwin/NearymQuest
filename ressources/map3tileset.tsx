<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.2" tiledversion="1.2.3" name="map2tileset" tilewidth="16" tileheight="16" tilecount="256" columns="16">
 <image source="map3tileset.png" trans="000000" width="256" height="256"/>
 <terraintypes>
  <terrain name="gravel" tile="17"/>
  <terrain name="water" tile="53"/>
  <terrain name="wheet" tile="23"/>
 </terraintypes>
 <tile id="0" terrain=",,,0"/>
 <tile id="1" terrain=",,0,0"/>
 <tile id="2" terrain=",,0,"/>
 <tile id="3" terrain="1,1,1,"/>
 <tile id="4" terrain="1,1,,"/>
 <tile id="5" terrain="1,1,,1"/>
 <tile id="6" terrain=",,,2">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="12" y="10" width="4" height="6"/>
  </objectgroup>
 </tile>
 <tile id="7" terrain=",,2,2">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="0" y="9" width="16" height="7"/>
  </objectgroup>
 </tile>
 <tile id="8" terrain=",,2,">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="0" y="11" width="5" height="5"/>
  </objectgroup>
 </tile>
 <tile id="9">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="collider" x="0" y="0" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="10">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="collider" x="0" y="0" width="14" height="16"/>
  </objectgroup>
 </tile>
 <tile id="11">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="collider" x="0" y="0" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="12">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="collider" x="0" y="0" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="13">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="14">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="15">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="16" terrain=",0,,0"/>
 <tile id="17" terrain="0,0,0,0"/>
 <tile id="18" terrain="0,,0,"/>
 <tile id="19" terrain="1,,1,"/>
 <tile id="21" terrain=",1,,1"/>
 <tile id="22" terrain=",2,,2">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="11" y="0" width="5" height="16"/>
  </objectgroup>
 </tile>
 <tile id="23" terrain="2,2,2,2">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="0" y="0" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="24" terrain="2,,2,">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="0" y="0" width="5" height="16"/>
  </objectgroup>
 </tile>
 <tile id="27">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="28">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="collider" x="2" y="0" width="14" height="16"/>
  </objectgroup>
 </tile>
 <tile id="29">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="30">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="collider" x="0" y="0" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="31">
  <properties>
   <property name="solid" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="collider" x="0" y="0" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="32" terrain=",0,,"/>
 <tile id="33" terrain="0,0,,"/>
 <tile id="34" terrain="0,,,"/>
 <tile id="35" terrain="1,,1,1"/>
 <tile id="36" terrain=",,1,1"/>
 <tile id="37" terrain=",1,1,1"/>
 <tile id="38" terrain=",2,,">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="11" y="0" width="5" height="11"/>
  </objectgroup>
 </tile>
 <tile id="39" terrain="2,2,,">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="0" y="0" width="16" height="11"/>
  </objectgroup>
 </tile>
 <tile id="40" terrain="2,,,">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="0" y="0" width="6" height="10"/>
  </objectgroup>
 </tile>
 <tile id="48" terrain="0,0,0,"/>
 <tile id="49" terrain="0,0,,0"/>
 <tile id="51" terrain=",,,1"/>
 <tile id="52" terrain=",,1,"/>
 <tile id="53" terrain="1,1,1,1">
  <properties>
   <property name="water" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="54" terrain="2,2,2,">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="0" y="0" width="16" height="11"/>
   <object id="2" type="hitbox" x="0" y="11" width="7" height="5"/>
  </objectgroup>
 </tile>
 <tile id="55" terrain="2,2,,2">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="0" y="0" width="16" height="10"/>
   <object id="2" type="hitbox" x="8" y="10" width="8" height="6"/>
  </objectgroup>
 </tile>
 <tile id="64" terrain="0,,0,0"/>
 <tile id="65" terrain=",0,0,0"/>
 <tile id="67" terrain=",1,,"/>
 <tile id="68" terrain="1,,,"/>
 <tile id="69">
  <properties>
   <property name="water" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="70" terrain="2,,2,2">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="0" y="0" width="6" height="8"/>
   <object id="2" type="hitbox" x="0" y="8" width="16" height="8"/>
  </objectgroup>
 </tile>
 <tile id="71" terrain=",2,2,2">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="0" y="8" width="16" height="8"/>
   <object id="2" type="hitbox" x="11" y="0" width="5" height="8"/>
  </objectgroup>
 </tile>
 <tile id="80">
  <properties>
   <property name="destructible" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="hitbox" x="3" y="8" width="9" height="5"/>
  </objectgroup>
 </tile>
 <tile id="81">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="solid" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="collider" x="2" y="6" width="12" height="9"/>
  </objectgroup>
 </tile>
 <tile id="96">
  <properties>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="97">
  <properties>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="98">
  <properties>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="112">
  <properties>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="113">
  <properties>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="114">
  <properties>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="129">
  <properties>
   <property name="inflamable" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="145">
  <properties>
   <property name="destructible" type="bool" value="true"/>
   <property name="inflamable" type="bool" value="true"/>
   <property name="solid" type="bool" value="true"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" type="collider" x="4" y="8" width="8" height="8"/>
  </objectgroup>
 </tile>
</tileset>
