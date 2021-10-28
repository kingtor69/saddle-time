--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4 (Ubuntu 13.4-4.pgdg20.04+1)
-- Dumped by pg_dump version 13.4 (Ubuntu 13.4-4.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: checkpoints; Type: TABLE; Schema: public; Owner: kingtor
--

CREATE TABLE public.checkpoints (
    id integer NOT NULL,
    user_id integer,
    checkpoint_display_name character varying,
    checkpoint_lat double precision NOT NULL,
    checkpoint_lng double precision NOT NULL
);


ALTER TABLE public.checkpoints OWNER TO kingtor;

--
-- Name: checkpoints_id_seq; Type: SEQUENCE; Schema: public; Owner: kingtor
--

CREATE SEQUENCE public.checkpoints_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.checkpoints_id_seq OWNER TO kingtor;

--
-- Name: checkpoints_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kingtor
--

ALTER SEQUENCE public.checkpoints_id_seq OWNED BY public.checkpoints.id;


--
-- Name: checkpoints_routes; Type: TABLE; Schema: public; Owner: kingtor
--

CREATE TABLE public.checkpoints_routes (
    id integer NOT NULL,
    route_id integer NOT NULL,
    checkpoint_id integer NOT NULL,
    route_order integer NOT NULL
);


ALTER TABLE public.checkpoints_routes OWNER TO kingtor;

--
-- Name: checkpoints_routes_id_seq; Type: SEQUENCE; Schema: public; Owner: kingtor
--

CREATE SEQUENCE public.checkpoints_routes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.checkpoints_routes_id_seq OWNER TO kingtor;

--
-- Name: checkpoints_routes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kingtor
--

ALTER SEQUENCE public.checkpoints_routes_id_seq OWNED BY public.checkpoints_routes.id;


--
-- Name: routes; Type: TABLE; Schema: public; Owner: kingtor
--

CREATE TABLE public.routes (
    id integer NOT NULL,
    route_name character varying(40),
    bike_type character varying(8),
    "timestamp" timestamp without time zone,
    user_id integer
);


ALTER TABLE public.routes OWNER TO kingtor;

--
-- Name: routes_id_seq; Type: SEQUENCE; Schema: public; Owner: kingtor
--

CREATE SEQUENCE public.routes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.routes_id_seq OWNER TO kingtor;

--
-- Name: routes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kingtor
--

ALTER SEQUENCE public.routes_id_seq OWNED BY public.routes.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: kingtor
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    first_name character varying,
    last_name character varying,
    profile_pic_image_url character varying,
    fav_bike character varying(40),
    bike_image_url character varying,
    default_bike_type character varying(8),
    default_geocode_lat double precision,
    default_geocode_lng double precision,
    units character varying(8)
);


ALTER TABLE public.users OWNER TO kingtor;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: kingtor
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO kingtor;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kingtor
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: checkpoints id; Type: DEFAULT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.checkpoints ALTER COLUMN id SET DEFAULT nextval('public.checkpoints_id_seq'::regclass);


--
-- Name: checkpoints_routes id; Type: DEFAULT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.checkpoints_routes ALTER COLUMN id SET DEFAULT nextval('public.checkpoints_routes_id_seq'::regclass);


--
-- Name: routes id; Type: DEFAULT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.routes ALTER COLUMN id SET DEFAULT nextval('public.routes_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: checkpoints; Type: TABLE DATA; Schema: public; Owner: kingtor
--

COPY public.checkpoints (id, user_id, checkpoint_display_name, checkpoint_lat, checkpoint_lng) FROM stdin;
1	\N	\N	35.191097	-106.582998
2	\N	\N	35.196087	-106.595115
3	\N	\N	35.135253	-106.607314
4	\N	\N	35.12229	-106.543057
5	\N	\N	35.191097	-106.582998
6	\N	\N	35.175451	-106.568183
7	\N	\N	35.12229	-106.543057
\.


--
-- Data for Name: checkpoints_routes; Type: TABLE DATA; Schema: public; Owner: kingtor
--

COPY public.checkpoints_routes (id, route_id, checkpoint_id, route_order) FROM stdin;
1	1	1	0
2	1	2	1
3	1	3	2
4	1	4	3
5	2	5	0
6	2	6	1
7	2	7	2
\.


--
-- Data for Name: routes; Type: TABLE DATA; Schema: public; Owner: kingtor
--

COPY public.routes (id, route_name, bike_type, "timestamp", user_id) FROM stdin;
1	good way home	regular	2021-10-28 18:03:12.394092	1
2	stop at the bike shop	regular	2021-10-28 18:03:12.394092	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: kingtor
--

COPY public.users (id, username, email, password, first_name, last_name, profile_pic_image_url, fav_bike, bike_image_url, default_bike_type, default_geocode_lat, default_geocode_lng, units) FROM stdin;
1	kingtor	tor@hearkitty.com	$2b$12$uf58RkLK/DatgprLGeIW4.qEOwFy.BoF6n.UuVTHkFKlF4CWFrvQG	Tor	Kingdon	/static/images/torRoadieProfilePic.jpg	The one I don't have yet....	/static/images/94422-50_ROUBAIX-COMP-REDTNT-METWHTSIL_HERO.webp	road	35.190564	-106.580526	metric
\.


--
-- Name: checkpoints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kingtor
--

SELECT pg_catalog.setval('public.checkpoints_id_seq', 7, true);


--
-- Name: checkpoints_routes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kingtor
--

SELECT pg_catalog.setval('public.checkpoints_routes_id_seq', 7, true);


--
-- Name: routes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kingtor
--

SELECT pg_catalog.setval('public.routes_id_seq', 2, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kingtor
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: checkpoints checkpoints_pkey; Type: CONSTRAINT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.checkpoints
    ADD CONSTRAINT checkpoints_pkey PRIMARY KEY (id);


--
-- Name: checkpoints_routes checkpoints_routes_pkey; Type: CONSTRAINT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.checkpoints_routes
    ADD CONSTRAINT checkpoints_routes_pkey PRIMARY KEY (id);


--
-- Name: routes routes_pkey; Type: CONSTRAINT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: checkpoints_routes checkpoints_routes_checkpoint_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.checkpoints_routes
    ADD CONSTRAINT checkpoints_routes_checkpoint_id_fkey FOREIGN KEY (checkpoint_id) REFERENCES public.checkpoints(id);


--
-- Name: checkpoints_routes checkpoints_routes_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.checkpoints_routes
    ADD CONSTRAINT checkpoints_routes_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(id);


--
-- Name: checkpoints checkpoints_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.checkpoints
    ADD CONSTRAINT checkpoints_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: routes routes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kingtor
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--
