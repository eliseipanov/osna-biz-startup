--
-- PostgreSQL database dump
--

\restrict LaboBxh1Gd9OV3PMfXPWyexCPpk6qmBkhBcATKC4nLuEqL5p6gRpNYlK3498TQV

-- Dumped from database version 15.14 (Debian 15.14-0+deb12u1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: availabilitystatus; Type: TYPE; Schema: public; Owner: osnafarm
--

CREATE TYPE public.availabilitystatus AS ENUM (
    'IN_STOCK',
    'OUT_OF_STOCK',
    'ON_REQUEST'
);


ALTER TYPE public.availabilitystatus OWNER TO osnafarm;

--
-- Name: languagepref; Type: TYPE; Schema: public; Owner: osnafarm
--

CREATE TYPE public.languagepref AS ENUM (
    'uk',
    'de'
);


ALTER TYPE public.languagepref OWNER TO osnafarm;

--
-- Name: orderstatus; Type: TYPE; Schema: public; Owner: osnafarm
--

CREATE TYPE public.orderstatus AS ENUM (
    'pending',
    'confirmed',
    'shipping',
    'done'
);


ALTER TYPE public.orderstatus OWNER TO osnafarm;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: osnafarm
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO osnafarm;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: osnafarm
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying,
    slug character varying,
    image_url character varying,
    description text,
    name_de character varying,
    description_de text,
    image_path character varying(255)
);


ALTER TABLE public.categories OWNER TO osnafarm;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: osnafarm
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO osnafarm;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osnafarm
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: farms; Type: TABLE; Schema: public; Owner: osnafarm
--

CREATE TABLE public.farms (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description_uk text,
    description_de text,
    location character varying(255),
    contact_info character varying(255),
    is_active boolean,
    image_path character varying(255)
);


ALTER TABLE public.farms OWNER TO osnafarm;

--
-- Name: farms_id_seq; Type: SEQUENCE; Schema: public; Owner: osnafarm
--

CREATE SEQUENCE public.farms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.farms_id_seq OWNER TO osnafarm;

--
-- Name: farms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osnafarm
--

ALTER SEQUENCE public.farms_id_seq OWNED BY public.farms.id;


--
-- Name: global_settings; Type: TABLE; Schema: public; Owner: osnafarm
--

CREATE TABLE public.global_settings (
    id integer NOT NULL,
    key character varying,
    value text
);


ALTER TABLE public.global_settings OWNER TO osnafarm;

--
-- Name: global_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: osnafarm
--

CREATE SEQUENCE public.global_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.global_settings_id_seq OWNER TO osnafarm;

--
-- Name: global_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osnafarm
--

ALTER SEQUENCE public.global_settings_id_seq OWNED BY public.global_settings.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: osnafarm
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    user_id integer,
    status public.orderstatus DEFAULT 'pending'::public.orderstatus,
    total_price double precision DEFAULT '0'::double precision,
    delivery_slot character varying(100),
    comment text,
    created_at timestamp without time zone DEFAULT now(),
    delivery_address text,
    contact_phone character varying
);


ALTER TABLE public.orders OWNER TO osnafarm;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: osnafarm
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO osnafarm;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osnafarm
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: osnafarm
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(255),
    price double precision,
    unit character varying(20) DEFAULT 'kg'::character varying,
    description text,
    category_id integer,
    name_de character varying,
    description_de text,
    sku character varying(50),
    availability_status public.availabilitystatus,
    farm_id integer,
    image_path character varying(255)
);


ALTER TABLE public.products OWNER TO osnafarm;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: osnafarm
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO osnafarm;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osnafarm
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: static_pages; Type: TABLE; Schema: public; Owner: osnafarm
--

CREATE TABLE public.static_pages (
    id integer NOT NULL,
    title character varying,
    slug character varying,
    content text,
    title_de character varying,
    content_de text,
    seo_title_uk character varying,
    seo_title_de character varying,
    seo_description_uk text,
    seo_description_de text
);


ALTER TABLE public.static_pages OWNER TO osnafarm;

--
-- Name: static_pages_id_seq; Type: SEQUENCE; Schema: public; Owner: osnafarm
--

CREATE SEQUENCE public.static_pages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.static_pages_id_seq OWNER TO osnafarm;

--
-- Name: static_pages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osnafarm
--

ALTER SEQUENCE public.static_pages_id_seq OWNED BY public.static_pages.id;


--
-- Name: translations; Type: TABLE; Schema: public; Owner: osnafarm
--

CREATE TABLE public.translations (
    id integer NOT NULL,
    key character varying,
    value_uk text,
    value_de text
);


ALTER TABLE public.translations OWNER TO osnafarm;

--
-- Name: translations_id_seq; Type: SEQUENCE; Schema: public; Owner: osnafarm
--

CREATE SEQUENCE public.translations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.translations_id_seq OWNER TO osnafarm;

--
-- Name: translations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osnafarm
--

ALTER SEQUENCE public.translations_id_seq OWNED BY public.translations.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: osnafarm
--

CREATE TABLE public.users (
    id integer NOT NULL,
    tg_id bigint,
    full_name character varying(255),
    phone character varying(20),
    address text,
    is_trusted boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT now(),
    password_hash character varying,
    is_admin boolean,
    email character varying,
    username character varying,
    language_pref public.languagepref,
    admin_notes text
);


ALTER TABLE public.users OWNER TO osnafarm;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: osnafarm
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO osnafarm;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osnafarm
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: farms id; Type: DEFAULT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.farms ALTER COLUMN id SET DEFAULT nextval('public.farms_id_seq'::regclass);


--
-- Name: global_settings id; Type: DEFAULT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.global_settings ALTER COLUMN id SET DEFAULT nextval('public.global_settings_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: static_pages id; Type: DEFAULT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.static_pages ALTER COLUMN id SET DEFAULT nextval('public.static_pages_id_seq'::regclass);


--
-- Name: translations id; Type: DEFAULT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.translations ALTER COLUMN id SET DEFAULT nextval('public.translations_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: osnafarm
--

COPY public.alembic_version (version_num) FROM stdin;
bad869430125
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: osnafarm
--

COPY public.categories (id, name, slug, image_url, description, name_de, description_de, image_path) FROM stdin;
2	Яловичина	rind	\N	Beef products from Homeyer	Rind	\N	\N
3	Ковбаси	wurst	\N	Sausages from Homeyer	Wurst	\N	\N
4	Мікс	mix	\N	Mixed meat products	Mix	\N	\N
1	Свинина	schwein	\N	Pork products from Homeyer	Schwein	\N	SvininaCategory.png
\.


--
-- Data for Name: farms; Type: TABLE DATA; Schema: public; Owner: osnafarm
--

COPY public.farms (id, name, description_uk, description_de, location, contact_info, is_active, image_path) FROM stdin;
1	Homeyer GmbH	\N	\N	Osnabrück	info@homeyer.de	t	Homeyer.png
\.


--
-- Data for Name: global_settings; Type: TABLE DATA; Schema: public; Owner: osnafarm
--

COPY public.global_settings (id, key, value) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: osnafarm
--

COPY public.orders (id, user_id, status, total_price, delivery_slot, comment, created_at, delivery_address, contact_phone) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: osnafarm
--

COPY public.products (id, name, price, unit, description, category_id, name_de, description_de, sku, availability_status, farm_id, image_path) FROM stdin;
1	Ошийок без кістки	5.49	кг	Fresh from Homeyer GmbH	1	Nacken ohne Knochen	\N	\N	IN_STOCK	1	\N
2	Фарш свинячий	4.5	кг	Fresh from Homeyer GmbH	1	Hackfleisch vom Schwein	\N	\N	IN_STOCK	1	\N
3	Шніцель / Печеня	5.9	кг	Fresh from Homeyer GmbH	1	Schnitzel / Braten	\N	\N	IN_STOCK	1	\N
4	Люммерстейк	6.9	кг	Fresh from Homeyer GmbH	1	Lummersteaks	\N	\N	IN_STOCK	1	\N
5	Філе (Свинина)	8.99	кг	Fresh from Homeyer GmbH	1	Filet (Schwein)	\N	\N	IN_STOCK	1	\N
6	Товсте ребро	4.9	кг	Fresh from Homeyer GmbH	1	Dicke Rippe	\N	\N	IN_STOCK	1	\N
7	Реберця (Spareribs)	5.5	кг	Fresh from Homeyer GmbH	1	Spareribs	\N	\N	IN_STOCK	1	\N
9	Грудинка	5.9	кг	Fresh from Homeyer GmbH	1	Bauchfleisch	\N	\N	IN_STOCK	1	\N
11	Котлета (Kotelett)	5.9	кг	Fresh from Homeyer GmbH	1	Kotelett	\N	\N	IN_STOCK	1	\N
8	Фарш асорті	5.8	кг	Fresh from Homeyer GmbH	4	Gehacktes halb & halb	\N	\N	IN_STOCK	1	\N
12	Яловичина без кістки	9.5	кг	Fresh from Homeyer GmbH	2	Rindfleisch ohne Knochen	\N	\N	IN_STOCK	1	\N
13	Яловичий фарш	7.2	кг	Fresh from Homeyer GmbH	2	Rinderhackfleisch	\N	\N	IN_STOCK	1	\N
14	Рулади (Яловичина)	13.5	кг	Fresh from Homeyer GmbH	2	Rouladen / Braten	\N	\N	IN_STOCK	1	\N
15	Супове м'ясо	8.5	кг	Fresh from Homeyer GmbH	2	Suppenfleisch	\N	\N	IN_STOCK	1	\N
16	Голяшка (Beinscheibe)	7.9	кг	Fresh from Homeyer GmbH	2	Beinscheibe	\N	\N	IN_STOCK	1	\N
17	Антрекот	19.5	кг	Fresh from Homeyer GmbH	2	Entrecote / Rumpsteak	\N	\N	IN_STOCK	1	\N
18	Філе (Яловичина)	29.9	кг	Fresh from Homeyer GmbH	2	Filet (Rind)	\N	\N	IN_STOCK	1	\N
19	Братвурст	8	кг	Fresh from Homeyer GmbH	3	Bratwurst	\N	\N	IN_STOCK	1	\N
20	Варена ковбаса	8.5	кг	Fresh from Homeyer GmbH	3	Fleischwurst	\N	\N	IN_STOCK	1	\N
21	Меттвурст	9.5	кг	Fresh from Homeyer GmbH	3	Mettwurst	\N	\N	IN_STOCK	1	\N
22	Печінкова ковбаса	8	кг	Fresh from Homeyer GmbH	3	Leberwurst	\N	\N	IN_STOCK	1	\N
23	Грютцвурст	7.5	кг	Fresh from Homeyer GmbH	3	Grützwurst	\N	\N	IN_STOCK	1	\N
10	Шинка для запікання	5.9	кг	\N	1	Schinkenbraten	Schinkenbraten von Homeyer GmbH	\N	IN_STOCK	1	SvininaProducten.png
\.


--
-- Data for Name: static_pages; Type: TABLE DATA; Schema: public; Owner: osnafarm
--

COPY public.static_pages (id, title, slug, content, title_de, content_de, seo_title_uk, seo_title_de, seo_description_uk, seo_description_de) FROM stdin;
\.


--
-- Data for Name: translations; Type: TABLE DATA; Schema: public; Owner: osnafarm
--

COPY public.translations (id, key, value_uk, value_de) FROM stdin;
1	welcome_message	Вітаємо в Osnabrück Farm Connect!	Willkommen bei Osnabrück Farm Connect!
2	catalog_button	🥩 Каталог	🥩 Katalog
3	cart_button	🛒 Кошик	🛒 Warenkorb
4	orders_button	📋 Мої замовлення	📋 Meine Bestellungen
5	profile_button	👤 Профіль	👤 Profil
6	producer_farm	Виробник/Ферма	Produzent/Farm
7	unit	Одиниця	Einheit
8	availability	Наявність	Verfügbarkeit
9	on_request	Під замовлення	Auf Anfrage
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: osnafarm
--

COPY public.users (id, tg_id, full_name, phone, address, is_trusted, created_at, password_hash, is_admin, email, username, language_pref, admin_notes) FROM stdin;
1	1957688188	Oleksii Marchenko	+4917682177891	An der Moorweide, 8\r\n49080, Osnabrück\r\nDeutschland	t	2026-01-11 23:36:09	scrypt:32768:8:1$V5SXBd1W9fr5VA5P$3caa7a470bc7d74c8bffbaf6852f4506a8937f5195f8f2df8faf3d774be308c2da832e387bc6fc88382c3728894b05486487aa795db8c7abadf5a4123ed58672	t	oleksii.pmarchenko@gmail.com	Olemara	uk	Головний менеджер
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osnafarm
--

SELECT pg_catalog.setval('public.categories_id_seq', 4, true);


--
-- Name: farms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osnafarm
--

SELECT pg_catalog.setval('public.farms_id_seq', 1, true);


--
-- Name: global_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osnafarm
--

SELECT pg_catalog.setval('public.global_settings_id_seq', 1, false);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osnafarm
--

SELECT pg_catalog.setval('public.orders_id_seq', 1, false);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osnafarm
--

SELECT pg_catalog.setval('public.products_id_seq', 23, true);


--
-- Name: static_pages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osnafarm
--

SELECT pg_catalog.setval('public.static_pages_id_seq', 1, false);


--
-- Name: translations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osnafarm
--

SELECT pg_catalog.setval('public.translations_id_seq', 9, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osnafarm
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: categories categories_slug_key; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_slug_key UNIQUE (slug);


--
-- Name: farms farms_name_key; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.farms
    ADD CONSTRAINT farms_name_key UNIQUE (name);


--
-- Name: farms farms_pkey; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.farms
    ADD CONSTRAINT farms_pkey PRIMARY KEY (id);


--
-- Name: global_settings global_settings_key_key; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.global_settings
    ADD CONSTRAINT global_settings_key_key UNIQUE (key);


--
-- Name: global_settings global_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.global_settings
    ADD CONSTRAINT global_settings_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: products products_sku_key; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_sku_key UNIQUE (sku);


--
-- Name: static_pages static_pages_pkey; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.static_pages
    ADD CONSTRAINT static_pages_pkey PRIMARY KEY (id);


--
-- Name: static_pages static_pages_slug_key; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.static_pages
    ADD CONSTRAINT static_pages_slug_key UNIQUE (slug);


--
-- Name: translations translations_key_key; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.translations
    ADD CONSTRAINT translations_key_key UNIQUE (key);


--
-- Name: translations translations_pkey; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.translations
    ADD CONSTRAINT translations_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_categories_id; Type: INDEX; Schema: public; Owner: osnafarm
--

CREATE INDEX ix_categories_id ON public.categories USING btree (id);


--
-- Name: ix_farms_id; Type: INDEX; Schema: public; Owner: osnafarm
--

CREATE INDEX ix_farms_id ON public.farms USING btree (id);


--
-- Name: ix_global_settings_id; Type: INDEX; Schema: public; Owner: osnafarm
--

CREATE INDEX ix_global_settings_id ON public.global_settings USING btree (id);


--
-- Name: ix_orders_id; Type: INDEX; Schema: public; Owner: osnafarm
--

CREATE INDEX ix_orders_id ON public.orders USING btree (id);


--
-- Name: ix_products_id; Type: INDEX; Schema: public; Owner: osnafarm
--

CREATE INDEX ix_products_id ON public.products USING btree (id);


--
-- Name: ix_static_pages_id; Type: INDEX; Schema: public; Owner: osnafarm
--

CREATE INDEX ix_static_pages_id ON public.static_pages USING btree (id);


--
-- Name: ix_translations_id; Type: INDEX; Schema: public; Owner: osnafarm
--

CREATE INDEX ix_translations_id ON public.translations USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: osnafarm
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_tg_id; Type: INDEX; Schema: public; Owner: osnafarm
--

CREATE UNIQUE INDEX ix_users_tg_id ON public.users USING btree (tg_id);


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: products products_farm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: osnafarm
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_farm_id_fkey FOREIGN KEY (farm_id) REFERENCES public.farms(id);


--
-- PostgreSQL database dump complete
--

\unrestrict LaboBxh1Gd9OV3PMfXPWyexCPpk6qmBkhBcATKC4nLuEqL5p6gRpNYlK3498TQV

