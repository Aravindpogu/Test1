package com.source;

public class Source {

	public int add (int a, int b){
		return a+b;
	}
	public static void main(String[] args) {
		Source src = new Source();
		System.out.println(src.add(10, -100));
	}

}
