LOAD CSV WITH HEADERS  FROM "file:///Ner_detail_hainan.csv" AS line  
CREATE (p:ZhizhuxiaItem{jud_id:line.jud_id,opps:line.opps,court:line.court,keywords:line.keywords,mon:line.mon,jud_text:line.jud_text});  


LOAD CSV  WITH HEADERS FROM "file:///wikidata_relation2.csv" AS line
MATCH (entity1:HudongItem{title:line.HudongItem}) , (entity2:NewNode{title:line.NewNode})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2)


LOAD CSV WITH HEADERS FROM "file:///Ner_relation.csv" AS line
MATCH (entity1:ZhizhuxiaItem{title:line.item1}) , (entity2:ZhizhuxiaItem{title:line.item2})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2);


// 1、详情表
LOAD CSV WITH HEADERS  FROM "file:///Ner_detail_hainan.csv" AS line  
CREATE (p:ZhizhuxiaItem{jud_id:line.jud_id,opps:line.opps,court:line.court,keywords:line.keywords,mon:line.mon,jud_text:line.jud_text});  

// 2、关系表
LOAD CSV WITH HEADERS FROM "file:///Ner_relation.csv" AS line
MATCH (entity1:ZhizhuxiaItem{title:line.item1}) , (entity2:ZhizhuxiaItem{title:line.item2})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2);

// 2、node表
LOAD CSV WITH HEADERS FROM "file:///Ner_node_hainan.csv" AS line
CREATE (:NewNode { title: line.title });


LOAD CSV  WITH HEADERS FROM "file:///wikidata_relation2.csv" AS line
MATCH (entity1:HudongItem{title:line.HudongItem}) , (entity2:NewNode{title:line.NewNode})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2)



// 3、关系表
LOAD CSV WITH HEADERS FROM "file:///Ner_relation.csv" AS line
MATCH (entity1:ZhizhuxiaItem{title:line.item1}) , (entity2:ZhizhuxiaItem{title:line.item2})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2);






// 数据导入分为四个步骤：

// 1、详情表
LOAD CSV WITH HEADERS  FROM "file:///Ner_detail_guizhou.csv" AS line  
CREATE (p:ZhizhuxiaItem{judgement_id:line.judgement_id,opps:line.opps,court:line.court,key_words:line.key_words,mon:line.mon,judgeText:line.judgeText});  

// 2、node表
LOAD CSV WITH HEADERS FROM "file:///Ner_node_guizhou.csv" AS line
CREATE (:NerNode { title: line.title });

// 3、关系表
LOAD CSV WITH HEADERS FROM "file:///Ner_relation_guizhou2.csv" AS line
MATCH (entity1:ZhizhuxiaItem{title:line.NerItem1}) , (entity2:ZhizhuxiaItem{title:line.NerItem2})
CREATE (entity1)-[:RELATION { type: line.relation }]->(entity2);

// 4、属性表
LOAD CSV WITH HEADERS FROM "file:///Ner_attributes.csv" AS line
MATCH (entity1:ZhizhuxiaItem{title:line.Entity}), (entity2:ZhizhuxiaItem{title:line.Attribute})
CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);
                                                            
LOAD CSV WITH HEADERS FROM "file:///Ner_attributes.csv" AS line
MATCH (entity1:ZhizhuxiaItem{title:line.Entity}), (entity2:NerNode{title:line.Attribute})
CREATE (entity1)-[:RELATION { type: line.AttributeName }]->(entity2);



//=================================
//     导入重新设计的表：主要原则是处理好关系的连续性，做到可扩展
//            1、一对多和多对一的关系
//=================================

// 1、person表
LOAD CSV WITH HEADERS FROM "file:///person.csv" AS line
CREATE (:Person {PersonID:line.PersonID,Name:line.Name,Gender:line.Gender,Birthday:line.Birthday,RegisterNum:line.RegisterNum,LegalPerson:line.LegalPerson,RegisterDate:line.RegisterDate,Location:line.Location,Stockholders:line.Stockholders});

LOAD CSV WITH HEADERS FROM "file:///person.csv" AS line
MERGE (person:Person {personID: line.PersonID}) ON CREATE SET person.Name = line.Name;

// 2、person_asset表
LOAD CSV WITH HEADERS FROM "file:///personasset.csv" AS line
CREATE (:PersonAsset {AssetID:line.AssetID,OtherAsset:line.OtherAsset,AssetDetail:line.AssetDetail,AssetUrl:line.AssetUrl});

// 3、sipai_detail表
LOAD CSV WITH HEADERS FROM "file:///sipaidetail.csv" AS line
CREATE (:SipaiDetail {JudgementID:line.JudgementID,Opps:line.Opps,Pros:line.Pros,Court:line.Court,KeyWords:line.KeyWords,Mon:line.Mon,JudgementText:line.JudgementText});

// 4、property表
LOAD CSV WITH HEADERS FROM "file:///sipaidetail.csv" AS line
CREATE (:Property {PropertyID:line.PropertyID, CategoryID:line.CategoryID,PropertyName:line.PropertyName,Creditor:line.Creditor,Debtor:line.Debtor});

// 5、categories表
LOAD CSV WITH HEADERS FROM "file:///categories.csv" AS line
CREATE (:Category {CategoryID:line.CategoryID, CategoryName:line.CategoryName,Description:line.Description});

// =============构建关系==============
// 1、原告被告和判决详情之间的关系
LOAD CSV WITH HEADERS FROM "file:///person.csv" AS line
MATCH (person:Person {PersonID: line.PersonID}),(sipaidetail: SipaiDetail {JudgementID: line.JudgementID})
MERGE (person)-[:DETAIL]->(sipaidetail);

// 2、



load csv with headers from "file:///person.csv" as line
match(from:Person{PersonID:line.PersonID}),(to:SipaiDetail{JudgementID:line.JudgementID})
merge(to)<-[r:DETAIL]-(from);
