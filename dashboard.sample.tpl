<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
<head> 
	<title>Dashboard</title> 
	<meta http-equiv="Content-type" content="text/html; charset=utf-8" /> 
	<meta http-equiv="Refresh" content="300" />
</head> 
<body> 
<ul>
{% for todo in todos %}
<li class="{{ todo.src }}">
	<a href="{{ todo.link }}" class="title">{{ todo.title }}</a>
	{% if todo.deadline %}
		<div class="deadline{% if todo.late %} late{% endif %}">
			Deadline: {{ todo.deadline }}</div>
	{% endif %}
	{% if todo.scheduled %}
		<div class="deadline{% if todo.late %} late{% endif %}">
			Scheduled: {{ todo.scheduled }}</div>
	{% endif %}
	<div class="subtitle">{{ todo.subtitle }}</div>
</li>
{% endfor %}
</ul>
</body> 
</html> 
