SELECT cp.checkpoint_display_name
    FROM checkpoints as cp
    JOIN route_checkpoints as rcp
    ON rcp.checkpoint_id = cp.id
    GROUP BY rcp.route_id, cp.checkpoint_display_name, rcp.route_order
    ORDER BY rcp.route_order;

--  checkpoint_display_name 
-- -------------------------
--  work
--  flying star paseo
--  7-11
--  outpost
-- (4 rows)


SELECT u.username, 
    r.route_name,
    cp.checkpoint_display_name
  FROM checkpoints as cp
  JOIN route_checkpoints as rcp
  ON rcp.checkpoint_id = cp.id
  JOIN routes as r
  ON rcp.route_id = r.id
  JOIN users as u 
  ON r.user_id = u.id
  GROUP BY rcp.route_id, 
    cp.checkpoint_display_name, 
    rcp.route_order,
    r.route_name,
    u.username
  ORDER BY rcp.route_order;

--  username |   route_name   | checkpoint_display_name 
-- ----------+----------------+-------------------------
--  kingtor  | Work to Hockey | work
--  kingtor  | Work to Hockey | flying star paseo
--  kingtor  | Work to Hockey | 7-11
--  kingtor  | Work to Hockey | outpost
-- (4 rows)

