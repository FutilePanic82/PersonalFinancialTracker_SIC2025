import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnalisisGastosComponent } from './analisis-gastos.component';

describe('AnalisisGastosComponent', () => {
  let component: AnalisisGastosComponent;
  let fixture: ComponentFixture<AnalisisGastosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AnalisisGastosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AnalisisGastosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
