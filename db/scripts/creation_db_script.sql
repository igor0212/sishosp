--OCCUPATION

CREATE TABLE public."Occupation" (
	"id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,	
	"name" varchar(50) NOT NULL,
	CONSTRAINT "PK_Occupation" PRIMARY KEY ("id")
);

INSERT INTO public."Occupation" ("name") VALUES('Doctor');
INSERT INTO public."Occupation" ("name") VALUES('Nurse');

--EMPLOYEE

CREATE TABLE public."Employee" (
	"id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,	
	"name" varchar(50) NOT NULL,
    "occupation_id" int4 NOT NULL,
	CONSTRAINT "PK_Employee" PRIMARY KEY ("id"),
    CONSTRAINT "FK_Employee_Occupation_Id" FOREIGN KEY ("occupation_id") REFERENCES public."Occupation"("id") ON DELETE RESTRICT
);

CREATE INDEX "IX_Employee_Occupation_Id" ON public."Employee" USING btree ("occupation_id");

INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Rebeka Magdalena', 1);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Sandra Iseul', 1);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Hira Andrej', 1);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Crescentius Lenz', 1);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Lochan Akakios', 1);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Agapitos Olaf', 2);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Milojica Xavi', 2);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Andrija Vijay', 2);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Bhaskara Donar', 2);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Batraz Vinay', 2);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Venetia Mariana', 2);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Júlia Sushila', 2);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Willidrud Martina', 2);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Jeannette Zheng', 2);
INSERT INTO public."Employee" ("name", "occupation_id") VALUES('Kumbukani Milda', 2);

--BLOCK

CREATE TABLE public."Block" (
	"id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,	
	"name" varchar(50) NOT NULL,
	CONSTRAINT "PK_Block" PRIMARY KEY ("id")
);

INSERT INTO public."Block" ("name") VALUES('A');
INSERT INTO public."Block" ("name") VALUES('B');
INSERT INTO public."Block" ("name") VALUES('C');

--BED

CREATE TABLE public."Bed" (
	"id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,	
	"name" varchar(50) NOT NULL,
    "block_id" int4 NOT NULL,
    "is_available" bool NOT NULL DEFAULT true,
	CONSTRAINT "PK_Bed" PRIMARY KEY ("id"),
    CONSTRAINT "FK_Bed_Block_Id" FOREIGN KEY ("block_id") REFERENCES public."Block"("id") ON DELETE RESTRICT
);

CREATE INDEX "IX_Bed_Block_Id" ON public."Bed" USING btree ("block_id");

INSERT INTO public."Bed" ("name", "block_id") VALUES('One', 1);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Two', 1);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Three', 1);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Four', 1);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Five', 1);

INSERT INTO public."Bed" ("name", "block_id") VALUES('One', 2);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Two', 2);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Three', 2);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Four', 2);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Five', 2);

INSERT INTO public."Bed" ("name", "block_id") VALUES('One', 3);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Two', 3);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Three', 3);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Four', 3);
INSERT INTO public."Bed" ("name", "block_id") VALUES('Five', 3);

--STATE

CREATE TABLE public."State" (
	"id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,	
	"name" varchar(50) NOT NULL,
	CONSTRAINT "PK_State" PRIMARY KEY ("id")
);

INSERT INTO public."State" ("name") VALUES('Light');
INSERT INTO public."State" ("name") VALUES('Moderate');
INSERT INTO public."State" ("name") VALUES('Serious');
INSERT INTO public."State" ("name") VALUES('Very Serious');

--PATIENT

CREATE TABLE public."Patient" (
	"id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,	
	"name" varchar(50) NOT NULL,
    "state_id" int4 NOT NULL,
    "bed_id" int4 NULL,
	CONSTRAINT "PK_Patient" PRIMARY KEY ("id"),
    CONSTRAINT "FK_Patient_State_Id" FOREIGN KEY ("state_id") REFERENCES public."State"("id") ON DELETE RESTRICT,
    CONSTRAINT "FK_Patient_Bed_Id" FOREIGN KEY ("bed_id") REFERENCES public."Bed"("id") ON DELETE RESTRICT
);

CREATE INDEX "IX_Patient_State_Id" ON public."Patient" USING btree ("state_id");
CREATE INDEX "IX_Patient_Bed_Id" ON public."Patient" USING btree ("bed_id");